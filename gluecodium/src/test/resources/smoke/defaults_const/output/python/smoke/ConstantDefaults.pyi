

from fire.SomeStruct import SomeStruct

from _native_base import _NativeBase


class ConstantDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field1: SomeStruct


    field2: SomeStruct

