

import typing

from _native_base import _NativeBase

import generated


class NullableOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    def foo(self, input: str): ...

    @typing.overload
    def foo(self, input: Optional[str]): ...

