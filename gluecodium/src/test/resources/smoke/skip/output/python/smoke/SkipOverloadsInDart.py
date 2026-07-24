

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class SkipOverloadsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(*args, **kwargs) -> SkipOverloadsInDart:
        """"""
        native_result = generated.SkipOverloadsInDart.make(*[_unwrap(a) for a in args])
        return SkipOverloadsInDart(native_result)


