

import typing

class StructWithOverloads:

    overloaded_accessors: int

    def overloaded_method(self) -> str:
        ...

    def overloaded_method(self, input: str) -> str:
        ...

    def overloaded_method(self, input_string: str, input_bool: bool) -> str:
        ...

