

import typing

from _native_base import _NativeBase

import generated


class OuterClassInnerClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo(self, input: str) -> str: ...

