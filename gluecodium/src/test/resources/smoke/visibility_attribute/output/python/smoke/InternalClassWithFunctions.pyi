

from smoke.InternalClassWithFunctions import InternalClassWithFunctions

from _native_base import _NativeBase


class InternalClassWithFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    def make(self) -> InternalClassWithFunctions:
        """"""
        return self._native.make()


    def make(self, foo: str) -> InternalClassWithFunctions:
        """"""
        return self._native.make(foo)

