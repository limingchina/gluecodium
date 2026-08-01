

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SkipOverloadsInDart(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(*args, **kwargs) -> SkipOverloadsInDart:
        native_result = generated.smoke_SkipOverloadsInDart.make(*[_unwrap(a) for a in args])
        return _get_or_create_wrapper(native_result, SkipOverloadsInDart)



