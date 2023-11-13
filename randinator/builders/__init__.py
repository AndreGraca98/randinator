# flake8: noqa
from typing import Any, Protocol

from .custom import *
from .simple import *


class Builder(Protocol):
    default: Any | None = None

    def __call__(self) -> Any:
        ...

    def build(self) -> Any:
        ...
