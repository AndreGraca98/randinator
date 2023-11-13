from typing import Literal

from isv2 import PydanticModel


class Meta(PydanticModel):
    type: str
    uuid: str
    active: bool
    country_code: str
    object_version: int
    schema_version: str
    source_event_id: str | None
    source_system: Literal["1.0", "1.1", "1.2", "1.3", "1.4"] | None
