

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from enum import Enum
import typing
from typing import Callable

class ParentClassWithImports:

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        ...

    @property
    def root_property(self) -> Callable[[int], None]:
        ...

    @root_property.setter
    def root_property(self, value: Callable[[int], None]) -> None:
        ...


