from collections.abc import Iterable
from importlib.resources.abc import Traversable


import importlib.resources
from pathlib import Path
from typing import Callable, final

DEFAULT_WORDS_FILE: Traversable = importlib.resources.files(__package__) / "words.txt"


def _read_words_file(file_path: str | Path | None) -> Iterable[str]:
    using_default_words = not file_path

    if using_default_words:
        fp = DEFAULT_WORDS_FILE.open("r")
    else:
        fp = open(file_path, "r")

    with fp:
        for line in fp:
            word = line.strip()
            if word:
                yield word


@final
class WordleGrepper:
    def __init__(self, file_path: str | Path | None = None) -> None:
        self._word_reader_func = lambda: _read_words_file(file_path)

    def grep(self, filter_func: "WordleFilterFunc") -> Iterable[str]:
        for word in self._word_reader_func():
            if filter_func(word):
                yield word


type WordleFilterFunc = Callable[[str], bool]


def filter_by_valid_wordle_characters() -> WordleFilterFunc:
    def filter_func(word: str) -> bool:
        return all("a" <= c <= "z" for c in word.lower())

    return filter_func


def filter_by_length(length: int) -> WordleFilterFunc:
    def filter_func(word: str) -> bool:
        return len(word) == length

    return filter_func


def filter_by_exact_letter(letter: str, position: int) -> WordleFilterFunc:
    letter = letter.lower()

    def filter_func(word: str) -> bool:
        return len(word) > position and word[position].lower() == letter

    return filter_func


def filter_by_misplaced_letter(letter: str, position: int) -> WordleFilterFunc:
    letter = letter.lower()

    def filter_func(word: str) -> bool:
        return letter in word.lower() and word[position].lower() != letter

    return filter_func


def filter_by_excluded_letter(letter: str) -> WordleFilterFunc:
    letter = letter.lower()

    def filter_func(word: str) -> bool:
        return letter not in word.lower()

    return filter_func


def combine_filters(*filters: WordleFilterFunc) -> WordleFilterFunc:
    def combined_filter(word: str) -> bool:
        return all(f(word) for f in filters)

    return combined_filter
