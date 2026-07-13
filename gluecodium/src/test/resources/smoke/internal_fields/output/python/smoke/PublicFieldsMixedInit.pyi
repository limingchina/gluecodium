


from _native_base import _NativeBase


class PublicFieldsMixedInit(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    public_field1: str


    public_field2: str


    internal_field: str

