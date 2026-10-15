

from smoke.ValidationUtils import ValidationUtils
from enum import Enum
import typing
from typing import Optional

class StructsWithMethods:
    def __init__(self) -> None: ...

    class Vector:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, x: float, y: float) -> None: ...

        x: float

        y: float

        def distance_to(self, other: StructsWithMethods.Vector) -> float:
            ...

        def add(self, other: StructsWithMethods.Vector) -> StructsWithMethods.Vector:
            ...

        @staticmethod
        def validate(x: float, y: float) -> bool:
            ...

        @typing.overload
        @staticmethod
        def create(x: float, y: float) -> StructsWithMethods.Vector:
            ...

        @typing.overload
        @staticmethod
        def create(other: StructsWithMethods.Vector) -> StructsWithMethods.Vector:
            ...

        @typing.overload
        @staticmethod
        def create(input: int) -> StructsWithMethods.Vector:
            ...
