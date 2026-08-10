

from enum import Enum
import typing

class StructWithOverloads:

    overloaded_accessors: int

    @typing.overload
    def overloaded_method(self) -> str:
        ...

    @typing.overload
    def overloaded_method(self, input: str) -> str:
        ...

    @typing.overload
    def overloaded_method(self, input_string: str, input_bool: bool) -> str:
        ...


