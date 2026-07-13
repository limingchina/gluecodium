

from smoke.NoCacheClass import NoCacheClass

from _native_base import _NativeBase


class NoCacheClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def make(self) -> NoCacheClass:
        """"""
        return self._native.make()


    def foo(self):
        """"""
        return self._native.foo()

