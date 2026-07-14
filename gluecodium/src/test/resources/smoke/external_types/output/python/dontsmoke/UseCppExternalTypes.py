

from __future__ import annotations

from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.ExternalEnum import ExternalEnum
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
        generated.UseCppExternalTypes.use_struct(input._native)

    @staticmethod
    def use_enum(input: ExternalEnum):
        """"""
        generated.UseCppExternalTypes.use_enum(input._native)

    @staticmethod
    def use_class(input: ClassWithOverloads):
        """"""
        generated.UseCppExternalTypes.use_class(input._native)

