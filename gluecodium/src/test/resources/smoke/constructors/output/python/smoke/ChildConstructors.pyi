

from smoke.Constructors import Constructors
from enum import Enum
import typing

class ChildConstructors(
    Constructors):

    @staticmethod
    def create() -> ChildConstructors:
        ...

    @staticmethod
    def create(other: Constructors) -> ChildConstructors:
        ...


