

from __future__ import annotations



from _native_base import _NativeBase

import generated


class NullableOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def foo(self, input: Optional[str]):
        """"""
        return self._native.foo(input)

