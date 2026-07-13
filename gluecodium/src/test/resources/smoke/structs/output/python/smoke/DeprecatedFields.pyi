


from _native_base import _NativeBase


class DeprecatedFields(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    normal_field1: str


    deprecated_field: str


    normal_field2: str

