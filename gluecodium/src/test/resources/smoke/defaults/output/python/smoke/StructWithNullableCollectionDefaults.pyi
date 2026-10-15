

from enum import Enum
import typing
from typing import Optional

class StructWithNullableCollectionDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, nullable_list_field: Optional[list[str]], nullable_map_field: Optional[dict[str, str]], nullable_set_field: Optional[set[str]]) -> None: ...

    nullable_list_field: Optional[list[str]]

    nullable_map_field: Optional[dict[str, str]]

    nullable_set_field: Optional[set[str]]
