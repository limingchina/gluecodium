

from smoke.Constructors import Constructors
from enum import Enum
import typing
from typing import Optional

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
