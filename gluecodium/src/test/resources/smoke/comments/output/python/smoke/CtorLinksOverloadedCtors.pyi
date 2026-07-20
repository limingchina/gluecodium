

import typing

from _native_base import _NativeBase

import generated


class CtorLinksOverloadedCtors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    @staticmethod
    def create(input: str) -> CtorLinksOverloadedCtors: ...

    @typing.overload
    @staticmethod
    def create(input: str, flag: bool) -> CtorLinksOverloadedCtors: ...

