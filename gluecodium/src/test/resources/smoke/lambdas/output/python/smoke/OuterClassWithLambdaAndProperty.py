

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


    @staticmethod
    def another_integer() -> int:
        """"""
        return generated.OuterClassWithLambdaAndProperty.another_integer()

