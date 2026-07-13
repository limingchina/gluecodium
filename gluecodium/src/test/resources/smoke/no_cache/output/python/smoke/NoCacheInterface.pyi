


from _native_base import _NativeBase


class NoCacheInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self):
        """"""
        return self._native.foo()

