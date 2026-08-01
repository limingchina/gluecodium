

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class OuterClassWithLambdaAndProperty(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @property
    def some_integer(self) -> int:
        return _wrap(self._native.some_integer, int)

    @some_integer.setter
    def some_integer(self, value: int):
        self._native.some_integer = _unwrap(value, int)

    @staticmethod
    def another_integer() -> int:
        return _wrap(generated.smoke_OuterClassWithLambdaAndProperty.another_integer(), int)

    @staticmethod
    def another_integer_set(value: int):
        generated.smoke_OuterClassWithLambdaAndProperty.another_integer_set(_unwrap(value, int))

    SomeInternalLambda = Callable[[int], int]
    
    

