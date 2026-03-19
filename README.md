# wordle-hints

A command-line tool for finding Wordle word candidates based on known letter constraints. Given what you know about exact positions, misplaced letters, and excluded letters, `wordle-hints` filters a word list and returns matching candidates.

## Description

Each Wordle guess gives you information about which letters are correct, misplaced, or absent. `wordle-hints` encodes that information as a compact filter string and narrows down the word list for you.

**Filter string format:** `Ab_Cd`

| Character              | Meaning                                                          |
| ---------------------- | ---------------------------------------------------------------- |
| Uppercase letter (`A`) | Exact match — this letter is correct at this position            |
| Lowercase letter (`a`) | Misplaced — this letter is in the word, but not at this position |
| Underscore (`_`)       | Unknown — no information about this position                     |

Multiple filter strings can be provided (one per guess) and are combined with AND logic — a word must satisfy all of them.

**Example:** After two guesses you know:

- The word has `R` in position 3 (exact)
- The word contains `E` but not in position 2 (misplaced)
- The letters `A`, `T`, `S` are not in the word

```bash
wordle-hints __R__ _e___ -x ATS
```

## Installation

Requires Python 3.14+ and [pipx](https://pipx.pypa.io).

```bash
pipx install git+https://github.com/fsufitch/wordle-hints.git
```

To upgrade to the latest version:

```bash
pipx upgrade wordle-hints
```

## Usage

```bash
wordle-hints [OPTIONS] FILTER [FILTER ...]
```

### Arguments

| Argument | Description                                                   |
| -------- | ------------------------------------------------------------- |
| `FILTER` | One or more filter strings (e.g. `__R__`, `_e___`). Required. |

### Options

| Option                            | Description                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| `-w`, `--words PATH`              | Path to a custom word list file (one word per line). Defaults to the built-in word list. |
| `-x`, `--exclude-letters LETTERS` | Letters known to be absent from the word (e.g. `-x ats`).                                |
| `-m`, `--max N`                   | Maximum number of results to print. Default: `20`. Use `0` for no limit.                 |
| `--help`                          | Show help and exit.                                                                      |

### Examples

Find all 5-letter words with `R` in position 3:

```bash
wordle-hints __R__
```

Combine two guesses and exclude known-absent letters:

```bash
wordle-hints __R__ _e___ -x ats
```

Use a custom word list and show all results:

```bash
wordle-hints -w /usr/share/dict/words -m 0 __R__
```

## Development Setup

Requires [uv](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/fsufitch/wordle-hints.git
cd wordle-hints

# Create a virtual environment and install the project with dev dependencies
uv venv
source .venv/bin/activate
uv sync --group dev
```

### Running the tool locally

```bash
wordle-hints --help
```

### Linting and formatting

```bash
flake8 wordle_hints/
black wordle_hints/
basedpyright wordle_hints/
```
