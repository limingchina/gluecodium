

from enum import Enum
import typing
from typing import Optional

class OrderInStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, struct_field: OrderInStruct.NestedStruct, enum_field: OrderInStruct.SomeEnum) -> None: ...

    struct_field: OrderInStruct.NestedStruct

    enum_field: OrderInStruct.SomeEnum

    class NestedStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class SomeEnum(Enum):

        FOO = 0
        BAR = 1
