

import typing

class ClassWithOverloads:

    def one_overload_not_exposed(self) -> str:
        ...

    def all_overloads_exposed(self, input: str) -> str:
        ...

    def all_overloads_exposed(self, input_list: list[str]) -> str:
        ...

    def all_overloads_exposed(self, input_string: str, input_bool: bool) -> str:
        ...

