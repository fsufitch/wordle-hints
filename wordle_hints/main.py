import sys
import click

from .words import (
    WordleFilterFunc,
    WordleGrepper,
    combine_filters,
    filter_by_exact_letter,
    filter_by_excluded_letter,
    filter_by_length,
    filter_by_misplaced_letter,
    filter_by_valid_wordle_characters,
)


def _print_error(message: str) -> None:
    click.secho(message, fg="orange", err=True)


@click.command()
@click.option(
    "-w",
    "--words",
    "file_path",
    type=click.Path(exists=True),
    help="Path to a file containing words, one per line. "
    + "Default: use built-in words file.",
)
@click.option(
    "-x",
    "--exclude-letters",
    "exclude_letters",
    help="Letters to exclude from the results.",
)
@click.option(
    "-m",
    "--max",
    "max_results",
    type=int,
    help="Maximum number of results to print. Set 0 for no limit. Beware huge outputs! Default: 20.",
    default=20,
)
@click.argument(
    "filters",
    nargs=-1,
)
def main(
    file_path: str | None,
    exclude_letters: str | None,
    max_results: int,
    filters: tuple[str, ...],
) -> None:
    """
    Print any words that match the given filters and excluded words.

    Filtering is applied as an "AND" operation, so a word must match all filters to be included in the results.

    Write filters as `Ab_Cd`, where A and C are exact letters, b and d are misplaced letters, and _ represents unknown letters.
    """
    if not filters:
        _print_error("No filters provided. Exiting.")
        sys.exit(1)

    filter_funcs = [_parse_filter_string(f) for f in filters]
    filter_func = combine_filters(*filter_funcs)

    if exclude_letters:
        exclude_letters_funcs = [filter_by_excluded_letter(c) for c in exclude_letters]
        exclude_letter_func = combine_filters(*exclude_letters_funcs)

        filter_func = combine_filters(filter_func, exclude_letter_func)

    wg = WordleGrepper(file_path)

    try:
        printed_count = 0
        for word in wg.grep(filter_func):
            click.echo(word)
            printed_count += 1
            if max_results > 0 and printed_count >= max_results:
                break
    except Exception as exc:
        _print_error(f"An error occurred: {exc}")
        sys.exit(1)


def _parse_filter_string(filter_str: str) -> WordleFilterFunc:
    filter_funcs: list[WordleFilterFunc] = [
        filter_by_valid_wordle_characters(),
        filter_by_length(len(filter_str)),
    ]
    for i, c in enumerate(filter_str):
        if c == "_":
            continue
        elif "A" <= c <= "Z":
            filter_funcs.append(filter_by_exact_letter(c, i))
        elif "a" <= c <= "z":
            filter_funcs.append(filter_by_misplaced_letter(c, i))
        else:
            raise ValueError(f"Invalid character '{c}' in filter string.")

    return combine_filters(*filter_funcs)


if __name__ == "__main__":
    main()
