


from _native_base import _NativeBase


class FieldConstructorsSkipDefault(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    string_field: str


    int_field: int

