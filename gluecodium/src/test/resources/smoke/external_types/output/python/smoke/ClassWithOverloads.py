

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ClassWithOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def one_overload_not_exposed(self) -> str:
        """"""
        return self._native.one_overload_not_exposed()


    def all_overloads_exposed(self, input: str) -> str:
        """"""
        return self._native.all_overloads_exposed(input)


    def all_overloads_exposed(self, input_list: list[str]) -> str:
        """"""
        return self._native.all_overloads_exposed(input_list)


    def all_overloads_exposed(self, input_string: str, input_bool: bool) -> str:
        """"""
        return self._native.all_overloads_exposed(input_string, input_bool)

