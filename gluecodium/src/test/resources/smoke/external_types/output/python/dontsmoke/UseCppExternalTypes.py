

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.EnumsExternal_Enum import EnumsExternal_Enum
from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct

from _native_base import _NativeBase

import generated


class UseCppExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def use_struct(input: StructsAnotherExternalStruct):
        """"""
        generated.dontsmoke_UseCppExternalTypes.use_struct(_unwrap(input, StructsAnotherExternalStruct))

    @staticmethod
    def use_enum(input: EnumsExternal_Enum):
        """"""
        generated.dontsmoke_UseCppExternalTypes.use_enum(_unwrap(input, EnumsExternal_Enum))

    @staticmethod
    def use_class(input: ClassWithOverloads):
        """"""
        generated.dontsmoke_UseCppExternalTypes.use_class(_unwrap(input, ClassWithOverloads))

