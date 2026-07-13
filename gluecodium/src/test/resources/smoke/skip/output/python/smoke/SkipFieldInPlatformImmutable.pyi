

from smoke.DummyStruct import DummyStruct

from _native_base import _NativeBase


class SkipFieldInPlatformImmutable(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    int_field: int


    string_field: DummyStruct


    bool_field: bool

