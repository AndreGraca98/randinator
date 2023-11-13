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

    builder_name: str = NotImplemented
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


__BUILDERS = dict()


def register(cls):
    assert (
        cls.builder_name is not NotImplemented
    ), f"builder_name must be provided for {cls}"
    assert isinstance(cls.builder_name, str)

    builders = get_builders()
    if cls.builder_name in get_builder_names():
        raise ValueError(
            f"{cls} with builder_name {cls.builder_name!r} already "
            f"registered for {builders[cls.builder_name]}"
        )
    if cls in builders:
        raise ValueError(f"Builder {cls} already registered")

    __BUILDERS[cls.builder_name] = cls
    return cls


def get_builders() -> dict[str, Builder]:
    return __BUILDERS


def get_builder_names() -> list[str]:
    return list(get_builders().keys())
    # return [v.builder_name for k, v in get_builders().items()]
