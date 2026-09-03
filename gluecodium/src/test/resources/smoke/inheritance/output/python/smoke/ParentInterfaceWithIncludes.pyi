

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ShouldNotInclude import ShouldNotInclude
from enum import Enum
import typing
from typing import Callable

class ParentInterfaceWithIncludes:

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        ...

    def not_in_java(self) -> ShouldNotInclude:
        ...

    @property
    def root_property(self) -> Callable[[int], None]:
        ...

    @root_property.setter
    def root_property(self, value: Callable[[int], None]) -> None:
        ...

    @property
    def not_in_java_property(self) -> ShouldNotInclude:
        ...

    @not_in_java_property.setter
    def not_in_java_property(self, value: ShouldNotInclude) -> None:
        ...


