

from smoke.AnotherExternalStruct import AnotherExternalStruct
from smoke.ExternalStruct import ExternalStruct

from _native_base import _NativeBase


class Structs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def get_external_struct(self) -> ExternalStruct:
        """"""
        return self._native.get_external_struct()


    def get_another_external_struct(self) -> AnotherExternalStruct:
        """"""
        return self._native.get_another_external_struct()

