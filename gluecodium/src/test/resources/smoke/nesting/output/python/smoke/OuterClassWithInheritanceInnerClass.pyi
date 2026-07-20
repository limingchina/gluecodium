

import typing

from _native_base import _NativeBase

import generated


class OuterClassWithInheritanceInnerClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def bar(self, input: str) -> str: ...

