

from enum import Enum
import typing

class EquatableStructWithInternalFields:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    public_field: str

    _internal_field: str

    _internal_list_field: list[str]

    _internal_map_field: dict[str, str]

    _internal_set_field: set[str]


