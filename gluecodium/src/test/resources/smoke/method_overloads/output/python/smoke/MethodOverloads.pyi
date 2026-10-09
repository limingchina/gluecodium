

from enum import Enum
import typing
from typing import Optional

class MethodOverloads:

    @typing.overload
    def is_boolean(self, input: bool) -> bool:
        ...

    @typing.overload
    def is_boolean(self, input: int) -> bool:
        ...

    @typing.overload
    def is_boolean(self, input: str) -> bool:
        ...

    @typing.overload
    def is_boolean(self, input: MethodOverloads.Point) -> bool:
        ...

    @typing.overload
    def is_boolean(self, input1: bool, input2: int, input3: str, input4: MethodOverloads.Point) -> bool:
        ...

    @typing.overload
    def is_boolean(self, input: list[str]) -> bool:
        ...

    @typing.overload
    def is_boolean(self, input: list[int]) -> bool:
        ...

    @typing.overload
    def is_boolean(self) -> bool:
        ...

    @typing.overload
    def is_float(self, input: str) -> bool:
        ...

    @typing.overload
    def is_float(self, input: list[int]) -> bool:
        ...

    class Point:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, x: float, y: float) -> None: ...

        x: float

        y: float



    StringArray = list[str]



    IntArray = list[int]
