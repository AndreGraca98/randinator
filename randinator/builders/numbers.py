import random
from dataclasses import dataclass
from decimal import Decimal
from logging import getLogger
from typing import Any

from typing_extensions import override

from randinator.builders.base import Builder

__all__ = [
    "IntegerBuilder",
    "IntegerStrBuilder",
    "FloatBuilder",
    "FloatStrBuilder",
    "PercentageBuilder",
    "DecimalBuilder",
    "BooleanBuilder",
]
_log = getLogger(__name__)


@dataclass(kw_only=True)
class IntegerBuilder(Builder):
    min_value: int
    max_value: int
    default: int | None = None
    default_type: type = int

    def __post_init__(self):
        super().__post_init__()
        assert isinstance(self.min_value, int), f"{self=}"
        assert isinstance(self.max_value, int), f"{self=}"
        assert self.min_value <= self.max_value, f"{self=}"

    def generate(self) -> int:
        return random.randint(self.min_value, self.max_value)

    def sanitize(self, value: Any) -> int:
        return int(value)


@dataclass(kw_only=True)
class IntegerStrBuilder(IntegerBuilder):
    default: str | None = None
    default_type: type = str

    def sanitize(self, value: Any) -> str:
        return str(value)


@dataclass(kw_only=True)
class FloatBuilder(Builder):
    min_value: float
    max_value: float
    decimal_places: int = 2
    default: float | None = None
    default_type: type = float

    def __post_init__(self):
        super().__post_init__()
        assert isinstance(self.min_value, (int, float)), f"{self=}"
        assert isinstance(self.max_value, (int, float)), f"{self=}"
        assert self.min_value <= self.max_value, f"{self=}"
        assert isinstance(self.decimal_places, int), f"{self=}"
        assert self.decimal_places >= 0, f"{self=}"

    def generate(self) -> float:
        return self.__round(random.uniform(self.min_value, self.max_value))

    def __round(self, value: float) -> float:
        return round(value, self.decimal_places)

    def sanitize(self, value: Any) -> float:
        return float(value)


@dataclass(kw_only=True)
class FloatStrBuilder(FloatBuilder):
    def sanitize(self, value: Any) -> str:
        return str(value)


@dataclass(kw_only=True)
class PercentageBuilder(FloatBuilder):
    min_value: float = 0.0
    max_value: float = 100.0

    def __post_init__(self):
        super().__post_init__()
        assert 0.0 <= self.min_value <= self.max_value <= 100.0, f"{self=}"


@dataclass(kw_only=True)
class DecimalBuilder(FloatBuilder):
    default: Decimal | None = None
    default_type: type = Decimal

    def __quantize(self, value: Decimal) -> Decimal:
        qtz_dec = Decimal(f"0.{'0' * self.decimal_places}")
        return value.quantize(qtz_dec, rounding="ROUND_HALF_UP")

    @override
    def __round(self, value: float) -> Decimal:
        return self.__quantize(Decimal(value))

    def sanitize(self, value: Any) -> Decimal:
        return self.__quantize(Decimal(value))


@dataclass(kw_only=True)
class BooleanBuilder(Builder):
    default: bool | None = None
    default_type: type = bool

    def generate(self) -> bool:
        return random.choice([True, False])

    def sanitize(self, value: Any) -> Any:
        return bool(value)
