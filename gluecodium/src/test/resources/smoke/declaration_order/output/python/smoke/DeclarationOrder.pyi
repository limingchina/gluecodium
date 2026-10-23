

from enum import Enum
import typing
from typing import Optional

class DeclarationOrder:
    def __init__(self) -> None: ...

    class MainStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, struct_field: DeclarationOrder.NestedStruct, type_def_field: int, struct_array_field: list[DeclarationOrder.NestedStruct], map_field: dict[int, list[DeclarationOrder.NestedStruct]], enum_field: DeclarationOrder.SomeEnum) -> None: ...

        struct_field: DeclarationOrder.NestedStruct

        type_def_field: int

        struct_array_field: list[DeclarationOrder.NestedStruct]

        map_field: dict[int, list[DeclarationOrder.NestedStruct]]

        enum_field: DeclarationOrder.SomeEnum



    class NestedStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class SomeEnum(Enum):

        FOO = 0
        BAR = 1



    SomeTypeDef = int



    ErrorCodeToMessageMap = dict[int, list[NestedStruct]]



    NestedStructArray = list[NestedStruct]
