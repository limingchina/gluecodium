

from smoke.ImmutableDefaultCtor import ImmutableDefaultCtor

from _native_base import _NativeBase


class MutableStructImmutableFieldsDefault(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    struct_field: ImmutableDefaultCtor


    int_field: int


    bool_field: bool

