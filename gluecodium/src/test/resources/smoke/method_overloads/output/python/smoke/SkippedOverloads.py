

from __future__ import annotations


from _native_base import _NativeBase

import generated


class SkippedOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> SkippedOverloads:
        """"""
        native_result = generated.SkippedOverloads.make()
        return SkippedOverloads(native_result)

    @staticmethod
    def make_for_dart(input: str) -> SkippedOverloads:
        """"""
        native_result = generated.SkippedOverloads.make_for_dart(input)
        return SkippedOverloads(native_result)

