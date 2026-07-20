

import typing

from _native_base import _NativeBase

import generated


class InternalClassWithFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo_bar(self): ...

    @typing.overload
    @staticmethod
    def make() -> InternalClassWithFunctions: ...

    @typing.overload
    @staticmethod
    def make(foo: str) -> InternalClassWithFunctions: ...

