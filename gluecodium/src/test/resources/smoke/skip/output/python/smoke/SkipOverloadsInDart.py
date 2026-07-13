

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SkipOverloadsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def make() -> SkipOverloadsInDart:
        """"""
        native_result = generated.SkipOverloadsInDart.make()
        return SkipOverloadsInDart(native_result)

    @staticmethod

    def make(input: str) -> SkipOverloadsInDart:
        """"""
        native_result = generated.SkipOverloadsInDart.make(input)
        return SkipOverloadsInDart(native_result)

