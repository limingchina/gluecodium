

from smoke.ParentClass import ParentClass

from _native_base import _NativeBase


class ChildClassFromClassOverloads(
    ParentClass)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def foo(self, input: float):
        """"""
        return self._native.foo(input)


    def bar(self, input: str):
        """"""
        return self._native.bar(input)


    def bar(self, input: float):
        """"""
        return self._native.bar(input)

