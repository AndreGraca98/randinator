from copy import deepcopy
from typing import Any, Self

import pydantic


class PydanticModel(pydantic.BaseModel):
    """Custom pydantic model for all schemas and payload messages"""

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        # strict=True,  # types should be enforced?
        validate_assignment=True,
        extra="forbid",
    )

    def as_dict(self, **kwargs) -> dict[str, Any]:
        """Return a dict with the model's data"""
        return deepcopy(self.model_dump(**kwargs))

    def as_json(self, **kwargs) -> dict[str, Any]:
        """Return a dict with the model's data, ready for json serialization"""
        kwargs.update(mode="json")
        return self.as_dict(**kwargs)

    def as_str(self, **kwargs) -> str:
        """Return a the model's data as a string. Can be used with `json.loads()`"""
        return self.model_dump_json(**kwargs)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**deepcopy(data))
