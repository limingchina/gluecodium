


from _native_base import _NativeBase


class FieldConstructorWithComment(_NativeBase):
    """SomeStruct"""

    def __init__(self, native):
        super().__init__(native)

    Some field
    string_field: str

