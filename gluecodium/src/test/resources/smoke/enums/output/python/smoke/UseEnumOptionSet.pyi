

from smoke.EnumOptionSet import EnumOptionSet
from enum import Enum
import typing
from typing import Optional

class UseEnumOptionSet:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, set_field: set[EnumOptionSet]) -> None: ...
    @typing.overload
    def __init__(self, set_field: set[EnumOptionSet], set_field_empty: set[EnumOptionSet], set_field_value: set[EnumOptionSet]) -> None: ...

    set_field: set[EnumOptionSet]

    set_field_empty: set[EnumOptionSet]

    set_field_value: set[EnumOptionSet]

    @staticmethod
    def round_trip(input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        ...
