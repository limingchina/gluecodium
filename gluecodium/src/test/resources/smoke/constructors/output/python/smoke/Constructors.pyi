

from smoke.ConstructorsConstructorExploded import ConstructorsConstructorExploded
from smoke.ConstructorsErrorEnum import ConstructorsErrorEnum
import typing

class Constructors:

    @staticmethod
    def create() -> Constructors:
        ...

    @staticmethod
    def create(other: Constructors) -> Constructors:
        ...

    @staticmethod
    def create(foo: str, bar: int) -> Constructors:
        ...

    @staticmethod
    def create(input: str) -> Constructors:
        ...

    @staticmethod
    def create(input: list[float]) -> Constructors:
        ...

    @staticmethod
    def create(input: int) -> Constructors:
        ...

