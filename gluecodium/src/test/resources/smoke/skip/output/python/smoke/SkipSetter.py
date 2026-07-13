

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SkipSetter(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, SkipSetter):
            super().__init__(native)
        else:
            super().__init__(generated.SkipSetter())


    @property
    def foo(self) -> str:
        """"""
        return self._native.foo

    @foo.setter
    def foo(self, value: str):
        self._native.foo = value

