import random
import string
from dataclasses import dataclass
from typing import Any

from randinator.builders.base import Builder, register

LETTERS = string.ascii_lowercase


@dataclass
@register
class TextBuilder(Builder):
    builder_name: str = "text"
    word_number: int = 1
    min_length: int = 5
    max_length: int = 10
    pre_word: str = ""
    post_word: str = ""
    default: str | None = None
    default_type: type = str

    def __post_init__(self):
        super().__post_init__()
        assert self.word_number > 0
        assert 0 < self.min_length <= self.max_length
        assert isinstance(self.pre_word, str)
        assert isinstance(self.post_word, str)

    def generate(self) -> str:
        words = " ".join(self.__word for _ in range(self.word_number))
        text = f"{self.pre_word} {words} {self.post_word}".strip()
        return text

    @property
    def __word(self) -> str:
        word_length: int = random.randint(self.min_length, self.max_length)
        return "".join(random.choice(LETTERS) for _ in range(word_length))

    def sanitize(self, value: Any) -> Any:
        return str(value)
