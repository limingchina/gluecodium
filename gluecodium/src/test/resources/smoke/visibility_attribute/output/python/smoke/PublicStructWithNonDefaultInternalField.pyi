


from _native_base import _NativeBase


class PublicStructWithNonDefaultInternalField(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    defaulted_field: int


    internal_field: str


    public_field: bool

