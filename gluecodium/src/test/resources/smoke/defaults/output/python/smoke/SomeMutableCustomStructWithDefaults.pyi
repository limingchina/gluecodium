


from _native_base import _NativeBase


class SomeMutableCustomStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    int_field: int


    string_field: str


    list_field: list[int]

