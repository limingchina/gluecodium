

from __future__ import annotations



from _native_base import _NativeBase

import generated


class InternalPropertyOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def foo(self) -> str:
        """"""
        return self._native.foo

    @foo.setter
    def foo(self, value: str):
        self._native.foo = value

