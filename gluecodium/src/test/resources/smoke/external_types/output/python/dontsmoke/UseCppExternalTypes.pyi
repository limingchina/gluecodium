

from smoke.AnotherExternalStruct import AnotherExternalStruct
from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.ExternalEnum import ExternalEnum

from _native_base import _NativeBase


class UseCppExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def use_struct(self, input: AnotherExternalStruct):
        """"""
        return self._native.use_struct(input)


    def use_enum(self, input: ExternalEnum):
        """"""
        return self._native.use_enum(input)


    def use_class(self, input: ClassWithOverloads):
        """"""
        return self._native.use_class(input)

