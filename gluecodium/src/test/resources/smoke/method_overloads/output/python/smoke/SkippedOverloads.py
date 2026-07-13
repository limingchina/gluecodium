

from smoke.SkippedOverloads import SkippedOverloads

class SkippedOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    def make(self) -> SkippedOverloads:
        """"""
        return self._native.make()


    def make_for_dart(self, input: str) -> SkippedOverloads:
        """"""
        return self._native.make_for_dart(input)

