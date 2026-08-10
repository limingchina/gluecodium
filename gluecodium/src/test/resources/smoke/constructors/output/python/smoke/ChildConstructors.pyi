

from smoke.Constructors import Constructors
from enum import Enum
import typing

class ChildConstructors(
    Constructors):

    @typing.overload
    @staticmethod
    def create() -> ChildConstructors:
        ...

    @typing.overload
    @staticmethod
    def create(other: Constructors) -> ChildConstructors:
        ...


