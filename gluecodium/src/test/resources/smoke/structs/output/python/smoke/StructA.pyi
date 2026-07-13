


from _native_base import _NativeBase


class StructA(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: list[StructB]

