

import typing

from _native_base import _NativeBase

import generated


class SkippedOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> SkippedOverloads: ...

    @staticmethod
    def make_for_dart(input: str) -> SkippedOverloads: ...

