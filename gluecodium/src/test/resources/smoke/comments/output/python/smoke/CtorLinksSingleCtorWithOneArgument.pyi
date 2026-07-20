

import typing

from _native_base import _NativeBase

import generated


class CtorLinksSingleCtorWithOneArgument(_NativeBase):
    """This class has just one constructor with one argument [create(Int)]."""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create(arg: int) -> CtorLinksSingleCtorWithOneArgument: ...

