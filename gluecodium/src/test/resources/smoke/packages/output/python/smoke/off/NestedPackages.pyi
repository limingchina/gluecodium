

from smoke.off.SomeStruct import SomeStruct

from _native_base import _NativeBase


class NestedPackages(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def basic_method(self, input: SomeStruct) -> SomeStruct:
        """"""
        return self._native.basic_method(input)

