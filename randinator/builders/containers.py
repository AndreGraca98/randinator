import random
from dataclasses import dataclass
from logging import getLogger
from typing import Any, Sequence

from randinator.builders.base import Builder

__all__ = [
    "DictBuilder",
    "ListBuilder",
    "PicklistBuilder",
]

_log = getLogger(__name__)


@dataclass(kw_only=True)
class ListBuilder(Builder):
    min_length: int = 0
    max_length: int = 0
    builder: Builder
    default: list[Any] | None = None
    default_type: type = list

    def __post_init__(self) -> None:
        assert isinstance(self.min_length, int), f"{self=}"
        assert isinstance(self.max_length, int), f"{self=}"
        assert self.min_length <= self.max_length, f"{self=}"
        assert isinstance(self.builder, Builder), f"{self=}"

    def generate(self) -> list:
        list_length = random.randint(self.min_length, self.max_length)
        return [self.builder.build() for _ in range(list_length)]

    def sanitize(self, value: Any) -> Any:
        return value


@dataclass(kw_only=True)
class DictBuilder(Builder):
    builders: dict[str, Builder]
    default: dict | None = None
    default_type: type = dict

    def __post_init__(self) -> None:
        super().__post_init__()
        assert isinstance(self.builders, dict), f"{self=}"
        assert all(isinstance(v, Builder) for v in self.builders.values()), f"{self=}"

    def generate(self) -> dict:
        return {k: v.build() for k, v in self.builders.items()}

    def sanitize(self, value: Any) -> Any:
        return value


@dataclass(kw_only=True)
class PicklistBuilder(Builder):
    """Chooses a random item from a picklist"""

    picklist: Sequence[Any]
    default: str | None = None
    default_type: type = str

    def __post_init__(self) -> None:
        assert isinstance(self.picklist, Sequence), f"{self=}"
        assert len(self.picklist) > 0, f"{self=}"

    def generate(self) -> str:
        return random.choice(self.picklist)

    def sanitize(self, value: Any) -> Any:
        return value
