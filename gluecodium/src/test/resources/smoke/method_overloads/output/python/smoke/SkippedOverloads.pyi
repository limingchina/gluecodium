

from smoke.SkippedOverloads import SkippedOverloads

from _native_base import _NativeBase


class SkippedOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def make(self) -> SkippedOverloads:
        """"""
        return self._native.make()


    def make_for_dart(self, input: str) -> SkippedOverloads:
        """"""
        return self._native.make_for_dart(input)

