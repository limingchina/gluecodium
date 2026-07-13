

from __future__ import annotations



from _native_base import _NativeBase

import generated


class OuterClassWithLambdaAndProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def some_integer(self) -> int:
        """"""
        return self._native.some_integer

    @some_integer.setter
    def some_integer(self, value: int):
        self._native.some_integer = value


    @property
    def another_integer(self) -> int:
        """"""
        return self._native.another_integer

    @another_integer.setter
    def another_integer(self, value: int):
        self._native.another_integer = value

