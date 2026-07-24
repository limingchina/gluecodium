

import typing

from _native_base import _NativeBase

import generated


class OuterClassWithLambdaAndProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @property
    def some_integer(self) -> int:
        """"""
        return _wrap(self._native.some_integer, int)

    @some_integer.setter
    def some_integer(self, value: int):
        self._native.some_integer = _unwrap(value, int)


    @staticmethod
    def another_integer() -> int:
        """"""
        return _wrap(generated.OuterClassWithLambdaAndProperty.another_integer(), int)

