from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    default: Any | None = None

    def assert_default_type(self, default_type: type) -> None:
        if self.default is not None:
            assert isinstance(self.default, default_type)

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
