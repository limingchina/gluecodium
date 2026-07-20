

import typing

from _native_base import _NativeBase

import generated


class SkipOverloadsInDart(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    @staticmethod
    def make() -> SkipOverloadsInDart: ...

    @typing.overload
    @staticmethod
    def make(input: str) -> SkipOverloadsInDart: ...

