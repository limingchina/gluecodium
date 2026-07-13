


from _native_base import _NativeBase


class StructWithList(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: list[StructWithList]

