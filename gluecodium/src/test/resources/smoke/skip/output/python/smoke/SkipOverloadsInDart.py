

from smoke.SkipOverloadsInDart import SkipOverloadsInDart

class SkipOverloadsInDart:
    """"""

    def __init__(self, native):
        self._native = native


    def make(self) -> SkipOverloadsInDart:
        """"""
        return self._native.make()


    def make(self, input: str) -> SkipOverloadsInDart:
        """"""
        return self._native.make(input)

