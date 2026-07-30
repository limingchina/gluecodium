

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class SkippedOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> SkippedOverloads:
        native_result = generated.smoke_SkippedOverloads.make()
        return _get_or_create_wrapper(native_result, SkippedOverloads)

    @staticmethod
    def make_for_dart(input: str) -> SkippedOverloads:
        native_result = generated.smoke_SkippedOverloads.make_for_dart(_unwrap(input, str))
        return _get_or_create_wrapper(native_result, SkippedOverloads)

