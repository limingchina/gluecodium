

from smoke.InnerStructWithDefaults import InnerStructWithDefaults

from _native_base import _NativeBase


class OuterStructWithFieldConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    outer_struct_field: InnerStructWithDefaults

