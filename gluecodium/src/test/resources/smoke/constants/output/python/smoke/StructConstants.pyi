

from enum import Enum
import typing
from typing import Optional

class StructConstants:

    class SomeStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, string_field: str, float_field: float) -> None: ...

        string_field: str

        float_field: float



    class NestingStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, struct_field: StructConstants.SomeStruct) -> None: ...

        struct_field: StructConstants.SomeStruct



    STRUCT_CONSTANT = SomeStruct("bar Buzz", 1.41)

    NESTING_STRUCT_CONSTANT = NestingStruct(SomeStruct("nonsense", -2.82))
