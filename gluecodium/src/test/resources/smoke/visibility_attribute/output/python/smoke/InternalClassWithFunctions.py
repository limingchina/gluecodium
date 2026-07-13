

from smoke.InternalClassWithFunctions import InternalClassWithFunctions

class InternalClassWithFunctions:
    """"""

    def __init__(self, native):
        self._native = native


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    def make(self) -> InternalClassWithFunctions:
        """"""
        return self._native.make()


    def make(self, foo: str) -> InternalClassWithFunctions:
        """"""
        return self._native.make(foo)

