

from enum import Enum
import typing
from typing import Optional

class EquatableStructWithInternalFields:
    def __eq__(self, other: object) -> bool: ...
    __hash__ = None  # type: ignore[assignment]
    def as_key(self) -> _gluecodium_key_736d6f6b652e457175617461626c6553747275637457697468496e7465726e616c4669656c6473: ...

    public_field: str

    _internal_field: str

    _internal_list_field: list[str]

    _internal_map_field: dict[str, str]

    _internal_set_field: set[str]



class _gluecodium_key_736d6f6b652e457175617461626c6553747275637457697468496e7465726e616c4669656c6473(EquatableStructWithInternalFields):
    def __hash__(self) -> int: ...  # type: ignore[override]
