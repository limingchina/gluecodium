

from smoke.SkipOverloadsInDart import SkipOverloadsInDart

from _native_base import _NativeBase


class SkipOverloadsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def make(self) -> SkipOverloadsInDart:
        """"""
        return self._native.make()


    def make(self, input: str) -> SkipOverloadsInDart:
        """"""
        return self._native.make(input)

