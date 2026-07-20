

from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.EnumsExternal_Enum import EnumsExternal_Enum
from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct
import typing

from _native_base import _NativeBase

import generated


class UseCppExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def use_struct(input: StructsAnotherExternalStruct): ...

    @staticmethod
    def use_enum(input: EnumsExternal_Enum): ...

    @staticmethod
    def use_class(input: ClassWithOverloads): ...

