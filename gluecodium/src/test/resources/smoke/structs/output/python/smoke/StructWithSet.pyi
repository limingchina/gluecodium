


from _native_base import _NativeBase


class StructWithSet(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: set[StructWithSet]

