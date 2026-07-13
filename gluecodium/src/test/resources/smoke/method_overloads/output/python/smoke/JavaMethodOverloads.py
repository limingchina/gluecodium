

from __future__ import annotations



from _native_base import _NativeBase

import generated


class JavaMethodOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def one(self, input: str):
        """"""
        return self._native.one(input)


    def two(self, input: list[str]):
        """"""
        return self._native.two(input)

