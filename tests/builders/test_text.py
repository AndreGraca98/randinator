import uuid

import pytest

from randinator.builders import FileTextBuilder, TextBuilder, Uuid4StrBuilder
from randinator.builders.text import DateStrBuilder


def test_text_builder():
    builder = TextBuilder(
        min_word_number=1, max_word_number=5, min_length=5, max_length=10
    )
    for _ in range(100):
        text = builder.build()
        assert isinstance(text, str)
        words = text.split()
        assert 1 <= len(words) <= 5
        assert all(5 <= len(word) <= 10 for word in words)


def test_file_text_builder_file_not_found():
    with pytest.raises(AssertionError):
        FileTextBuilder(
            filepath="nonexistent.txt", min_word_number=1, max_word_number=5
        )


def test_file_text_builder_file_empty(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("")
    with pytest.raises(AssertionError):
        FileTextBuilder(filepath=file, min_word_number=1, max_word_number=5)


def test_uuid4_str_builder_valid_uuid():
    builder = Uuid4StrBuilder()
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, str)
        assert len(value) == 36
        assert str(uuid.UUID(value, version=4)) == value


def test_date_str_builder_valid_date():
    builder = DateStrBuilder()
    for _ in range(100):
        value = builder.build()
        assert isinstance(value, str)
        assert len(value) == 10
        assert value[4] == "-"
        assert value[7] == "-"
        assert isinstance(builder.sanitize(value), str)
