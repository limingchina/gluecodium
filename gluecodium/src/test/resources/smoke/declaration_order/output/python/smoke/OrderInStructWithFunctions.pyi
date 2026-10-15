

from enum import Enum
import typing
from typing import Optional

class OrderInStructWithFunctions:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, some_field: str) -> None: ...

    some_field: str

    def do_stuff(self, struct_foo: OrderInStructWithFunctions.NestedStruct) -> OrderInStructWithFunctions.SomeEnum:
        ...

    class NestedStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class SomeEnum(Enum):

        FOO = 0
        BAR = 1
