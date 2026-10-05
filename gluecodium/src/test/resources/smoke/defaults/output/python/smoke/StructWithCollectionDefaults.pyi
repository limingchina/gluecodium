

from enum import Enum
import typing
from typing import Optional

class StructWithCollectionDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, empty_list_field: list[str], empty_map_field: dict[str, str], empty_set_field: set[str], list_field: list[str], map_field: dict[str, str], set_field: set[str]) -> None: ...

    empty_list_field: list[str]

    empty_map_field: dict[str, str]

    empty_set_field: set[str]

    list_field: list[str]

    map_field: dict[str, str]

    set_field: set[str]
