

import typing

from _native_base import _NativeBase

import generated


class ClassWithOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def one_overload_not_exposed(self) -> str: ...

    @typing.overload
    def all_overloads_exposed(self, input: str) -> str: ...

    @typing.overload
    def all_overloads_exposed(self, input_list: list[str]) -> str: ...

    @typing.overload
    def all_overloads_exposed(self, input_string: str, input_bool: bool) -> str: ...

