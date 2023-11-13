import random
import string
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from randinator.builders.base import Builder

__all__ = [
    "TextBuilder",
    "NumberTextBuilder",
    "IntegerBuilder",
    "FloatBuilder",
    "BooleanBuilder",
    "ListBuilder",
    "KeyBuilder",
    "DictBuilder",
    "DecimalBuilder",
]


@dataclass
class NumberBuilder(Builder):
    min_value: int = -1000
    max_value: int = 1000
    default: int | None = None

    def __post_init__(self):
        assert self.min_value <= self.max_value
        if self.default is not None:
            assert isinstance(self.default, int)

    def build(self) -> int:
        if self.default is not None:
            return self.default
        value = random.randint(self.min_value, self.max_value)
        return self.sanitize(value)

    def sanitize(self, value: Any) -> int:
        return int(value)


@dataclass
class NumberStrBuilder(NumberBuilder):
    def sanitize(self, value: Any) -> str:
        return str(value)


class TextBuilder(Builder):
    """Builds a text string. If no default is provided,
    a random string is generated. Can be forced to generate
    a specific string by providing default. Can customize the
    number of words, min and max length of words, and pre and post words."""

    LETTERS = string.ascii_lowercase

    def __init__(
        self,
        *,
        word_number: int = 1,
        min_length: int = 5,
        max_length: int = 10,
        pre_word: str = "",
        post_word: str = "",
        default: str | None = None,
    ):
        assert word_number > 0
        self.word_number = word_number
        assert min_length <= max_length
        self.min_length = min_length
        self.max_length = max_length
        assert isinstance(pre_word, str)
        self.pre_word = pre_word
        assert isinstance(post_word, str)
        self.post_word = post_word
        if default is not None:
            assert isinstance(default, str)
        self.default = default

    def build(self) -> str:
        if self.default is not None:
            return self.default
        words = " ".join(self._get_word() for _ in range(self.word_number))
        text = f"{self.pre_word} {words} {self.post_word}".strip()
        return text

    def _get_word(self) -> str:
        return "".join(random.choice(self.LETTERS) for _ in range(self._get_length()))

    def _get_length(self) -> int:
        return random.randint(self.min_length, self.max_length)


class NumberTextBuilder(TextBuilder):
    LETTERS = string.digits


class IntegerBuilder(Builder):
    """Builds an integer. If no default is provided, a random integer
    is generated. Can be forced to generate a specific integer by
    providing default. Can customize the min and max value."""

    def __init__(
        self, *, min_value: int = 0, max_value: int = 100, default: int | None = None
    ):
        assert min_value <= max_value
        self.min_value = min_value
        self.max_value = max_value
        if default is not None:
            assert isinstance(default, int)
        self.default = default

    def build(self) -> int:
        if self.default is not None:
            return self.default
        return random.randint(self.min_value, self.max_value)


class FloatBuilder(Builder):
    """Builds a float. If no default is provided, a random float is generated.
    Can be forced to generate a specific float by providing default.
    Can customize the min and max value."""

    def __init__(
        self,
        *,
        min_value: float = 0.0,
        max_value: float = 100.0,
        decimal_places: int = 2,
        default: float | None = None,
    ):
        assert min_value <= max_value
        self.min_value = min_value
        self.max_value = max_value
        assert isinstance(decimal_places, int)
        self.decimal_places = decimal_places
        if default is not None:
            assert isinstance(default, float)
        self.default = default

    def build(self) -> float:
        if self.default is not None:
            return self.default
        return self._round(self._get_random_value())

    def _round(self, value: float) -> float:
        return round(value, self.decimal_places)

    def _get_random_value(self) -> float:
        return random.uniform(self.min_value, self.max_value)


class DecimalBuilder(FloatBuilder):
    def _round(self, value: float) -> Decimal:
        rounding = f"0.{'0' * self.decimal_places}"
        return Decimal(value).quantize(Decimal(rounding), rounding="ROUND_HALF_UP")


class BooleanBuilder(Builder):
    """Builds a boolean. If no default is provided, a random boolean is generated."""

    def __init__(self, *, default: bool | None = None) -> None:
        if default is not None:
            assert isinstance(default, bool)
        self.default = default

    def build(self) -> bool:
        if self.default is not None:
            return self.default
        return random.choice([True, False])


class ListBuilder(Builder):
    """Builds a list. If no default is provided, an empty list is generated.
    Can be customized to generate a list of specific length, and with specific
    items. If no builder is provided, None is generated"""

    def __init__(
        self,
        *,
        min_length: int = 0,
        max_length: int = 0,
        builder: Builder | None = None,
        default: list | None = None,
    ) -> None:
        assert min_length <= max_length
        self.min_length = min_length
        self.max_length = max_length
        self.item_builder = builder
        if default is not None:
            assert isinstance(default, list)
        self.default = default

    def build(self) -> list:
        if self.default is not None:
            return self.default
        return [self._get_item() for _ in range(self._get_length())]

    def _get_length(self) -> int:
        return random.randint(self.min_length, self.max_length)

    def _get_item(self) -> Any:
        if self.item_builder is None:
            return None
        return self.item_builder.build()


class KeyBuilder(Builder):
    def __init__(
        self,
        *,
        key_length: int = 0,
        key_base: str = "key",
        default: str | None = None,
    ) -> None:
        self.key_length = key_length
        assert isinstance(key_base, str)
        self.key_base = key_base
        if default is not None:
            assert isinstance(default, str)
        self.default = default

    def build(self) -> list:
        if self.default is not None:
            return [self.default for _ in range(self.key_length)]
        return [f"{self.key_base}_{i}" for i in range(self.key_length)]


class DictBuilder(Builder):
    """Builds a dict. If no default is provided, an empty dict is generated."""

    def __init__(
        self,
        *,
        builders: dict[str, Builder] | None = None,
        default: dict | None = None,
    ) -> None:
        self.builders = builders
        if default is not None:
            assert isinstance(default, dict)
        self.default = default

    def build(self) -> dict:
        if self.default is not None:
            return self.default
        if self.builders is None:
            return {}
        return {k: v.build() for k, v in self.builders.items()}
