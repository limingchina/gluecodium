


from _native_base import _NativeBase


class CppRefReturnTypeStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def string_ref(self) -> str:
        """"""
        return self._native.string_ref()

