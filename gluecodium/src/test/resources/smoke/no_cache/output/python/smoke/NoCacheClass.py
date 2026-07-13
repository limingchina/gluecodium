

from smoke.NoCacheClass import NoCacheClass

class NoCacheClass:
    """"""

    def __init__(self, native):
        self._native = native


    def make(self) -> NoCacheClass:
        """"""
        return self._native.make()


    def foo(self):
        """"""
        return self._native.foo()

