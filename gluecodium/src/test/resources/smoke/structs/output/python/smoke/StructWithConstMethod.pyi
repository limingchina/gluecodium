


from _native_base import _NativeBase


class StructWithConstMethod(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    string_field: str


    def double_const(self) -> float:
        """"""
        return self._native.double_const()

