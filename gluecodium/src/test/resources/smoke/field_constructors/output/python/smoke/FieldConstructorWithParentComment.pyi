


from _native_base import _NativeBase


class FieldConstructorWithParentComment(_NativeBase):
    """SomeStruct"""

    def __init__(self, native):
        super().__init__(native)


    string_field: str

