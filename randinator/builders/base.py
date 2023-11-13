from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Builder(ABC):
    """Base class for all builders. Provides a default value and type for all builders.
    If a default is provided, it must be of the same type as the default_type and
    it will be used instead of generating a random value, otherwise, a random
    value will be generated.
    """

    default: Any = NotImplemented
    default_type: type = NotImplemented

    def __post_init__(self) -> None:
        self.__assert_default_type()

    def __assert_default_type(self) -> None:
        msg = lambda attr: f"{attr} must be provided for {self.__class__}"  # noqa: E731
        assert self.default is not NotImplemented, msg("default")
        assert self.default_type is not NotImplemented, msg("default_type")
        if self.default is not None:
            assert isinstance(self.default, self.default_type)

    def __call__(self) -> Any:
        return self.build()

    def build(self) -> Any:
        if self.default is not None:
            return self.default
        return self.sanitize(self.generate())

    @abstractmethod
    def generate(self) -> Any:
        """Generate a random value."""

    @abstractmethod
    def sanitize(self, value: Any) -> Any:
        """Sanitizes a value to match the builder's expectations."""
