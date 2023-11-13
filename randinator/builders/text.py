import random
import string
import uuid
from dataclasses import dataclass
from datetime import date
from logging import getLogger
from pathlib import Path
from typing import Any

from randinator.builders.base import Builder

__all__ = [
    "TextBuilder",
    "FileTextBuilder",
    "Uuid4StrBuilder",
    "DateStrBuilder",
]


_log = getLogger(__name__)

LETTERS = string.ascii_lowercase


@dataclass(kw_only=True)
class TextBuilder(Builder):
    min_word_number: int
    max_word_number: int
    min_length: int = 5
    max_length: int = 10
    pre_word: str = ""
    post_word: str = ""
    default: str | None = None
    default_type: type = str

    def __post_init__(self):
        super().__post_init__()
        assert isinstance(self.min_word_number, int), f"{self=}"
        assert isinstance(self.max_word_number, int), f"{self=}"
        assert 0 < self.min_word_number <= self.max_word_number, f"{self=}"
        assert isinstance(self.min_length, int), f"{self=}"
        assert isinstance(self.max_length, int), f"{self=}"
        assert 0 < self.min_length <= self.max_length, f"{self=}"
        assert isinstance(self.pre_word, str), f"{self=}"
        assert isinstance(self.post_word, str), f"{self=}"

    def generate(self) -> str:
        nwords = random.randint(self.min_word_number, self.max_word_number)
        words = " ".join(self.__word for _ in range(nwords))
        text = f"{self.pre_word} {words} {self.post_word}".strip()
        return text

    @property
    def __word(self) -> str:
        word_length: int = random.randint(self.min_length, self.max_length)
        return "".join(random.choice(LETTERS) for _ in range(word_length))

    def sanitize(self, value: Any) -> Any:
        return str(value)


@dataclass(kw_only=True)
class FileTextBuilder(Builder):
    filepath: Path | str
    min_word_number: int
    max_word_number: int
    pre_word: str = ""
    post_word: str = ""
    default: str | None = None
    default_type: type = str

    def __post_init__(self) -> None:
        super().__post_init__()
        assert isinstance(self.min_word_number, int), f"{self=}"
        assert isinstance(self.max_word_number, int), f"{self=}"
        assert 0 < self.min_word_number <= self.max_word_number, f"{self=}"
        assert isinstance(self.pre_word, str), f"{self=}"
        assert isinstance(self.post_word, str), f"{self=}"
        assert isinstance(self.filepath, (Path, str)), f"{self=}"
        assert Path(self.filepath).is_file(), f"{self.filepath} does not exist"
        assert Path(self.filepath).read_text(), f"{self.filepath} is empty"

    def generate(self) -> str:
        nwords = random.randint(self.min_word_number, self.max_word_number)
        words = " ".join(self.__word for _ in range(nwords))
        text = f"{self.pre_word} {words} {self.post_word}".strip()
        return text

    @property
    def __word(self) -> str:
        return random.choice(Path(self.filepath).read_text().split("\n"))

    def sanitize(self, value: Any) -> Any:
        return str(value)


@dataclass(kw_only=True)
class Uuid4StrBuilder(Builder):
    default: str | None = None
    default_type: type = str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.default is not None:
            assert isinstance(self.default, str)
            # Coerce to valid uuid
            self.default = str(uuid.UUID(self.default, version=4))

    def generate(self) -> str:
        return str(uuid.uuid4())

    def sanitize(self, value: Any) -> Any:
        return str(value)


@dataclass(kw_only=True)
class DateStrBuilder(Builder):
    """Builds a date string in isoformat. If no default is provided,
    a random date is generated. Can be forced to generate a specific
    date by providing year, month or day."""

    year: int | None = None
    month: int | None = None
    day: int | None = None
    default: str | None = None
    default_type: type = str

    def __post_init__(self) -> None:
        super().__post_init__()
        assert self.year is None or isinstance(self.year, int), f"{self=}"
        assert self.month is None or isinstance(self.month, int), f"{self=}"
        assert self.day is None or isinstance(self.day, int), f"{self=}"
        y = self.year if self.year is not None else 2000
        m = self.month if self.month is not None else 1
        d = self.day if self.day is not None else 1
        date(y, m, d)  # If date can be created it's a valid combination
        if self.default is not None:
            assert isinstance(self.default, str)
            date.fromisoformat(self.default)  # Check if valid date

    def generate(self) -> str:
        return self.__random_date.isoformat()

    @property
    def __random_date(self) -> date:
        while True:
            try:
                return date(**self.__random_date_kwargs)
            except ValueError:
                "Invalid date, try again."

    @property
    def __random_date_kwargs(self) -> dict[str, int]:
        year = self.year if self.year is not None else random.randint(1970, 2999)
        month = self.month if self.month is not None else random.randint(1, 12)
        day = self.day if self.day is not None else random.randint(1, 31)
        return dict(year=year, month=month, day=day)

    def sanitize(self, value: Any) -> Any:
        return str(value)
