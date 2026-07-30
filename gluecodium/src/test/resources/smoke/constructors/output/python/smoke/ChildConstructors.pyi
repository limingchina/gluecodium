

from smoke.Constructors import Constructors
from smoke.ConstructorsConstructorExploded import ConstructorsConstructorExploded
from smoke.ConstructorsErrorEnum import ConstructorsErrorEnum
import typing

class ChildConstructors(
    Constructors):

    @staticmethod
    def create() -> ChildConstructors:
        ...

    @staticmethod
    def create(other: Constructors) -> ChildConstructors:
        ...

