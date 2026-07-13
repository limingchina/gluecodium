

from smoke.ExampleStruct import ExampleStruct

from _native_base import _NativeBase


class PropertiesInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def struct_property(self) -> ExampleStruct:
        """"""
        return self._native.struct_property


