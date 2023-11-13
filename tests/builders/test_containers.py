from randinator.builders import DictBuilder, ListBuilder, PicklistBuilder
from randinator.builders.numbers import IntegerBuilder


def test_list_builder():
    builder = ListBuilder(
        min_length=1, max_length=5, builder=IntegerBuilder(min_value=0, max_value=10)
    )
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, list)
        assert 1 <= len(value) <= 5
        assert all(0 <= v <= 10 for v in value)


def test_dict_builder():
    builder = DictBuilder(builders={"a": IntegerBuilder(min_value=0, max_value=10)})
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, dict)
        assert "a" in value
        assert isinstance(value["a"], int)
        assert 0 <= value["a"] <= 10


def test_picklist_builder():
    builder = PicklistBuilder(picklist=["a", "b", "c"])
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, str)
        assert value in ["a", "b", "c"]
