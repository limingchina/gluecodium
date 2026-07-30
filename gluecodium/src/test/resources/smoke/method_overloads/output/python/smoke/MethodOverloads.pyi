

from smoke.MethodOverloadsPoint import MethodOverloadsPoint
import typing

class MethodOverloads:

    def is_boolean(self, input: bool) -> bool:
        ...

    def is_boolean(self, input: int) -> bool:
        ...

    def is_boolean(self, input: str) -> bool:
        ...

    def is_boolean(self, input: MethodOverloadsPoint) -> bool:
        ...

    def is_boolean(self, input1: bool, input2: int, input3: str, input4: MethodOverloadsPoint) -> bool:
        ...

    def is_boolean(self, input: list[str]) -> bool:
        ...

    def is_boolean(self, input: list[int]) -> bool:
        ...

    def is_boolean(self) -> bool:
        ...

    def is_float(self, input: str) -> bool:
        ...

    def is_float(self, input: list[int]) -> bool:
        ...

