import random
import uuid
import warnings
from datetime import date
from io import TextIOWrapper
from typing import Any

__all__ = [
    "Uuid4StrBuilder",
    "DateStrBuilder",
    "PicklistBuilder",
    "WordBuilder",
    "PhraseBuilder",
]


class Uuid4StrBuilder:
    """Builds a uuid4 string. If no default is provided,
    a random uuid4 is generated."""

    def __init__(self, *, default: str | None = None) -> None:
        if default is not None:
            assert isinstance(default, str)
            default = str(uuid.UUID(default, version=4))  # Check if valid uuid
        self.default = default

    def __call__(self) -> str:
        return self.build()

    def build(self) -> str:
        if self.default is not None:
            return self.default
        return str(uuid.uuid4())


class DateStrBuilder:
    """Builds a date string in isoformat. If no default is provided,
    a random date is generated. Can be forced to generate a specific
    date by providing year, month or day."""

    def __init__(
        self,
        *,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        default: str | None = None,
    ) -> None:
        self.year = year
        self.month = month
        self.day = day
        if default is not None:
            assert isinstance(default, str)
            date.fromisoformat(default)  # Check if valid date
        self.default = default

    def __call__(self) -> str:
        return self.build()

    def build(self) -> str:
        if self.default is not None:
            return self.default
        return self._get_random_date().isoformat()

    def _get_random_date(self) -> date:
        while True:
            try:
                d = date(**self._get_random_date_kwargs())
                break
            except ValueError:
                "Invalid date, try again."
        return d

    def _get_random_date_kwargs(self) -> dict[str, int]:
        year = self.year if self.year is not None else random.randint(2000, 2030)
        month = self.month if self.month is not None else random.randint(1, 12)
        day = self.day if self.day is not None else random.randint(1, 31)
        return dict(year=year, month=month, day=day)


class PicklistBuilder:
    """Chooses a random item from a picklist. If no default
    is provided, a random item is chosen."""

    def __init__(
        self,
        *,
        picklist: list[Any],
        default: str | None = None,
    ) -> None:
        self.picklist = picklist
        if default is not None:
            assert isinstance(default, str)
        self.default = default

    def __call__(self) -> str:
        return self.build()

    def build(self) -> str:
        if self.default is not None:
            return self.default
        return random.choice(self.picklist)


class WordBuilder:
    """Builds a word. If no default is provided,
    a random word is generated from a list of words. If a
    file is provided, it will be read and split by newlines.
    If a string is provided, it will be split by whitespace.
    """

    def __init__(
        self,
        *,
        words: str | list[str] | TextIOWrapper,
        default: str | None = None,
    ) -> None:
        if isinstance(words, (list, tuple)):
            pass
        elif isinstance(words, str):
            warnings.warn("Words should be a list of words, not a string.")
            words = words.split()
        elif isinstance(words, TextIOWrapper):
            words = list(filter(lambda w: w.strip(), words.read().split("\n")))
        else:
            raise TypeError("words must be str, list or TextIOWrapper")
        self.words = words
        if default is not None:
            assert isinstance(default, str)
        self.default = default

    def __call__(self) -> str:
        return self.build()

    def build(self) -> str:
        if self.default is not None:
            return self.default
        return self._get_word()

    def _get_word(self) -> str:
        return random.choice(self.words)


class PhraseBuilder:
    """Builds a phrase. If no default is provided, a random
    phrase is generated from a word builder."""

    def __init__(
        self,
        *,
        word_builder: WordBuilder,
        word_number: int = 3,
        default: str | None = None,
    ) -> None:
        self.word_builder = word_builder
        assert word_number > 0
        self.word_number = word_number
        if default is not None:
            assert isinstance(default, str)
        self.default = default

    def __call__(self) -> str:
        return self.build()

    def build(self) -> str:
        if self.default is not None:
            return self.default
        words = " ".join(self.word_builder.build() for _ in range(self.word_number))
        return words
