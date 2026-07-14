

from smoke.MethodOverloadsPoint import MethodOverloadsPoint


from _native_base import _NativeBase

import generated


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

    def is_boolean(self, input: MethodOverloadsPoint) -> bool:
        """"""
        return self._native.is_boolean(input._native)

    def is_boolean(self, input1: bool, input2: int, input3: str, input4: MethodOverloadsPoint) -> bool:
        """"""
        return self._native.is_boolean(input1, input2, input3, input4._native)

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

