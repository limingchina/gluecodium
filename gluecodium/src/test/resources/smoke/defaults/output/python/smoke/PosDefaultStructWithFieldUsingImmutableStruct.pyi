

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults

from _native_base import _NativeBase


class PosDefaultStructWithFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    some_field1: ImmutableStructWithDefaults

