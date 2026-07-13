


from _native_base import _NativeBase


class InternalPropertyOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def foo(self) -> str:
        """"""
        return self._native.foo


