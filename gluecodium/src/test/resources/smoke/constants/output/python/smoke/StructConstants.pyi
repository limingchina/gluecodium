

from enum import Enum
import typing
from typing import Optional

class StructConstants:

    class SomeStruct:

        string_field: str

        float_field: float



    class NestingStruct:

        struct_field: StructConstants.SomeStruct



    STRUCT_CONSTANT = SomeStruct("bar Buzz", 1.41)

    NESTING_STRUCT_CONSTANT = NestingStruct(SomeStruct("nonsense", -2.82))
