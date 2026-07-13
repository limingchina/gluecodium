


from _native_base import _NativeBase


class FieldConstructorWithExcluded(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    Some field
    string_field: str

