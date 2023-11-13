import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from randinator.builders.base import Builder

__all__ = []


@dataclass
class NumberBuilder(Builder):
    min_value: int = -1000
    max_value: int = 1000
    default: int | None = None
    default_type: type = int

    def __post_init__(self):
        super().__post_init__()
        assert self.min_value <= self.max_value

    def generate(self) -> int:
        return random.randint(self.min_value, self.max_value)

    def sanitize(self, value: Any) -> int:
        return int(value)


@dataclass
class NumberPositiveBuilder(NumberBuilder):
    min_value: int = 0
    max_value: int = 1000


@dataclass
class NumberNegativeBuilder(NumberBuilder):
    min_value: int = -1000
    max_value: int = 0


@dataclass
class NumberStrBuilder(NumberBuilder):
    default: str | None = None
    default_type: type = str

    def sanitize(self, value: Any) -> str:
        return str(value)


@dataclass
class FloatBuilder(Builder):
    min_value: float = -1000.0
    max_value: float = 1000.0
    decimal_places: int = 2
    default: float | None = None
    default_type: type = float

    def __post_init__(self):
        super().__post_init__()
        assert self.min_value <= self.max_value
        assert isinstance(self.decimal_places, int)

    def generate(self) -> float:
        return self._round(random.uniform(self.min_value, self.max_value))

    def _round(self, value: float) -> float:
        return round(value, self.decimal_places)

    def sanitize(self, value: Any) -> float:
        return float(value)


@dataclass
class FloatPositiveBuilder(FloatBuilder):
    min_value: float = 0.0
    max_value: float = 1000.0


@dataclass
class FloatNegativeBuilder(FloatBuilder):
    min_value: float = -1000.0
    max_value: float = 0.0


@dataclass
class FloatStrBuilder(FloatBuilder):
    def sanitize(self, value: Any) -> str:
        return str(value)


@dataclass
class PercentageBuilder(FloatBuilder):
    min_value: float = 0.0
    max_value: float = 100.0
    decimal_places: int = 2

    def __post_init__(self):
        super().__post_init__()
        assert 0.0 <= self.min_value <= self.max_value <= 100.0


@dataclass
class DecimalBuilder(FloatBuilder):
    default: Decimal | None = None
    default_type: type = Decimal

    def _round(self, value: float) -> Decimal:
        rounding = f"0.{'0' * self.decimal_places}"
        return Decimal(value).quantize(Decimal(rounding), rounding="ROUND_HALF_UP")

    def sanitize(self, value: Any) -> Decimal:
        return Decimal(value)
