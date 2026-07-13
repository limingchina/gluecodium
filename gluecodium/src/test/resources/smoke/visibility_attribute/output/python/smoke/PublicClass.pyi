

from smoke.InternalStruct import InternalStruct

from _native_base import _NativeBase


class PublicClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def internal_method(self, input: InternalStruct) -> InternalStruct:
        """"""
        return self._native.internal_method(input)


    @property
    def internal_struct_property(self) -> InternalStruct:
        """"""
        return self._native.internal_struct_property


