

from enum import Enum
import typing

class ClassWithOverloads:

    def one_overload_not_exposed(self) -> str:
        ...

    @typing.overload
    def all_overloads_exposed(self, input: str) -> str:
        ...

    @typing.overload
    def all_overloads_exposed(self, input_list: list[str]) -> str:
        ...

    @typing.overload
    def all_overloads_exposed(self, input_string: str, input_bool: bool) -> str:
        ...


