

from __future__ import annotations


from _native_base import _NativeBase

import generated


class SkipOverloadsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(*args, **kwargs) -> SkipOverloadsInDart:
        """"""
        native_result = generated.SkipOverloadsInDart.make(*[getattr(a, "_native", a) for a in args])
        return SkipOverloadsInDart(native_result)


