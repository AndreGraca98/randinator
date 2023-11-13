from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import getLogger
from typing import Any

__all__ = [
    "Builder",
    "get_builders",
    "get_builder",
    "get_builder_names",
    "register",
]

_log = getLogger(__name__)


@dataclass
class Builder(ABC):
    """Base class for all builders. Provides a default value and type for all builders.
    If a default is provided, it must be of the same type as the default_type and
    it will be used instead of generating a random value, otherwise, a random
    value will be generated.
    """

    default: Any = NotImplemented
    default_type: type = NotImplemented

    def __init_subclass__(cls, *args, **kwargs):
        """Registers the builder class with the name of the class normalized."""

        def normalize_name(name: str) -> str:
            assert "builder" in name.lower(), f"cls with {name=} must contain 'builder'"
            __name = ""
            for i, letter in enumerate(name):
                __name += f"_{letter}" if letter.isupper() and i > 0 else letter
            return __name.lower().replace("builder", "").strip("_")

        # Set the normalized name for the builder, used for registering
        name = normalize_name(cls.__name__)
        setattr(cls, "__normalized_name", name)
        register(cls)

    def __post_init__(self) -> None:
        self.__assert_defaults()

    def __assert_defaults(self) -> None:
        msg = lambda attr: f"{attr} must be provided for {self.__class__}"  # noqa: E731
        assert self.default is not NotImplemented, msg("default")
        assert self.default_type is not NotImplemented, msg("default_type")
        if self.default is not None:
            assert isinstance(self.default, self.default_type), f"{self=}"

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


def register(cls: type[Builder]):
    """Registers a builder class. The builder_name must
    be provided and must be unique"""
    builder_name = cls.__normalized_name  # type: ignore
    _log.debug(f"Registering {cls} with name {builder_name}")

    assert builder_name is not NotImplemented, f"name must be provided for {cls}"
    assert isinstance(builder_name, str)

    builders = get_builders()
    if builder_name in get_builder_names():
        raise ValueError(
            f"Tried to register {cls} with the same "
            f"name={builder_name!r} for {builders[builder_name]}"
        )
    if cls in builders:
        raise ValueError(f"Builder {cls} already registered")

    __BUILDERS[builder_name] = cls
    return cls


def get_builders() -> dict[str, Builder]:
    """Returns a dict of all registered builders"""
    return __BUILDERS


def get_builder(name: str) -> Builder:
    """Returns a builder by name"""
    return get_builders()[name]


def get_builder_names() -> list[str]:
    """Returns a list of all registered builder names"""
    return list(get_builders().keys())
