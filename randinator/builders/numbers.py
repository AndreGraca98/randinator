import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from typing_extensions import override

from randinator.builders.base import Builder


@dataclass
class IntegerBuilder(Builder):
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
class IntegerStrBuilder(IntegerBuilder):
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
        assert self.decimal_places >= 0

    def generate(self) -> float:
        return self.__round(random.uniform(self.min_value, self.max_value))

    def __round(self, value: float) -> float:
        return round(value, self.decimal_places)

    def sanitize(self, value: Any) -> float:
        return float(value)


@dataclass
class FloatStrBuilder(FloatBuilder):
    def sanitize(self, value: Any) -> str:
        return str(value)


@dataclass
class PercentageBuilder(FloatBuilder):
    min_value: float = 0.0
    max_value: float = 100.0

    def __post_init__(self):
        super().__post_init__()
        assert 0.0 <= self.min_value <= self.max_value <= 100.0


@dataclass
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
