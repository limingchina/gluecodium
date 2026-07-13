


from _native_base import _NativeBase


class FieldConstructorWithDeprecationOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    string_field: str

