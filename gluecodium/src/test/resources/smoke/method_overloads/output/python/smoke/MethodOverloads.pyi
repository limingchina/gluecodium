

from smoke.Point import Point
from smoke.list[int] import list[int]
from smoke.list[str] import list[str]

from _native_base import _NativeBase


class MethodOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def is_boolean(self, input: bool) -> bool:
        """"""
        return self._native.is_boolean(input)


    def is_boolean(self, input: int) -> bool:
        """"""
        return self._native.is_boolean(input)


    def is_boolean(self, input: str) -> bool:
        """"""
        return self._native.is_boolean(input)


    def is_boolean(self, input: Point) -> bool:
        """"""
        return self._native.is_boolean(input)


    def is_boolean(self, input1: bool, input2: int, input3: str, input4: Point) -> bool:
        """"""
        return self._native.is_boolean(input1, input2, input3, input4)


    def is_boolean(self, input: list[str]) -> bool:
        """"""
        return self._native.is_boolean(input)


    def is_boolean(self, input: list[int]) -> bool:
        """"""
        return self._native.is_boolean(input)


    def is_boolean(self) -> bool:
        """"""
        return self._native.is_boolean()


    def is_float(self, input: str) -> bool:
        """"""
        return self._native.is_float(input)


    def is_float(self, input: list[int]) -> bool:
        """"""
        return self._native.is_float(input)

