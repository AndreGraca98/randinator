from decimal import Decimal

from randinator.builders import (
    BooleanBuilder,
    DecimalBuilder,
    FloatBuilder,
    FloatStrBuilder,
    IntegerBuilder,
    IntegerStrBuilder,
    PercentageBuilder,
)


def test_integer_builder():
    builder = IntegerBuilder(min_value=0, max_value=10)
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, int)
        assert 0 <= value <= 10


def test_integer_str_builder():
    builder = IntegerStrBuilder(min_value=0, max_value=10)
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, str)
        assert 0 <= int(value) <= 10


def test_float_builder():
    builder = FloatBuilder(min_value=0.0, max_value=10.0)
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, float)
        assert 0.0 <= value <= 10.0


def test_float_str_builder():
    builder = FloatStrBuilder(min_value=0.0, max_value=10.0)
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, str)
        assert 0.0 <= float(value) <= 10.0


def test_percentage_builder():
    builder = PercentageBuilder()
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, float)
        assert 0.0 <= value <= 100.0


def test_decimal_builder():
    builder = DecimalBuilder(min_value=0.0, max_value=10.0)
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, Decimal), f"{type(value)} {value}"
        assert 0.0 <= value <= 10.0, f"{value}"


def test_boolean_builder_values():
    builder = BooleanBuilder()
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, bool)
