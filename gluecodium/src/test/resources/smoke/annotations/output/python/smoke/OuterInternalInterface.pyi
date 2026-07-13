


from _native_base import _NativeBase


class OuterInternalInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def some_function(self) -> int:
        """"""
        return self._native.some_function()

