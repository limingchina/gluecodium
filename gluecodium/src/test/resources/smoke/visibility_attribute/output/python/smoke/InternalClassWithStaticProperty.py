

from __future__ import annotations



from _native_base import _NativeBase

import generated


class InternalClassWithStaticProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def foo_bar(self) -> str:
        """"""
        return self._native.foo_bar

    @foo_bar.setter
    def foo_bar(self, value: str):
        self._native.foo_bar = value

