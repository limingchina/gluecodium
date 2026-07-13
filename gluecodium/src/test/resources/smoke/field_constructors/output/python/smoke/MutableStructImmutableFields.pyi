

from smoke.ImmutableStructNoClash import ImmutableStructNoClash

from _native_base import _NativeBase


class MutableStructImmutableFields(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    struct_field: ImmutableStructNoClash


    int_field: int


    bool_field: bool

