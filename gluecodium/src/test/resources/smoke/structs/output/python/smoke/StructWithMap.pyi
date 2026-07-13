


from _native_base import _NativeBase


class StructWithMap(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: dict[str, StructWithMap]

