

from smoke.MethodOverloadsPoint import MethodOverloadsPoint
import typing

from _native_base import _NativeBase

import generated


class MethodOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    def is_boolean(self, input: bool) -> bool: ...

    @typing.overload
    def is_boolean(self, input: int) -> bool: ...

    @typing.overload
    def is_boolean(self, input: str) -> bool: ...

    @typing.overload
    def is_boolean(self, input: MethodOverloadsPoint) -> bool: ...

    @typing.overload
    def is_boolean(self, input1: bool, input2: int, input3: str, input4: MethodOverloadsPoint) -> bool: ...

    @typing.overload
    def is_boolean(self, input: list[str]) -> bool: ...

    @typing.overload
    def is_boolean(self, input: list[int]) -> bool: ...

    @typing.overload
    def is_boolean(self) -> bool: ...

    @typing.overload
    def is_float(self, input: str) -> bool: ...

    @typing.overload
    def is_float(self, input: list[int]) -> bool: ...

