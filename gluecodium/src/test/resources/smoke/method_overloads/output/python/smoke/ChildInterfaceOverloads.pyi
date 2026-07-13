

from smoke.ParentInterface import ParentInterface

from _native_base import _NativeBase


class ChildInterfaceOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def bar(self, input: str):
        """"""
        return self._native.bar(input)

