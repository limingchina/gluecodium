

from smoke.ValidationUtils import ValidationUtils
from enum import Enum
import typing
from typing import Optional

class StructsWithMethodsInterface:

    class Vector3:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, x: float, y: float, z: float) -> None: ...

        x: float

        y: float

        z: float

        def distance_to(self, other: StructsWithMethodsInterface.Vector3) -> float:
            ...

        def add(self, other: StructsWithMethodsInterface.Vector3) -> StructsWithMethodsInterface.Vector3:
            ...

        @staticmethod
        def validate(x: float, y: float, z: float) -> bool:
            ...

        @typing.overload
        @staticmethod
        def create(input: str) -> StructsWithMethodsInterface.Vector3:
            ...

        @typing.overload
        @staticmethod
        def create(other: StructsWithMethodsInterface.Vector3) -> StructsWithMethodsInterface.Vector3:
            ...



    class StructWithStaticMethodsOnly:
        def __init__(self) -> None: ...

        @staticmethod
        def do_stuff():
            ...
