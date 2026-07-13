


from _native_base import _NativeBase


class StructWithSomeDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    int_field: int


    string_field: str

