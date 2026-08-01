

from another.SomeCoolClassType import SomeCoolClassType
from enum import Enum
import typing

class ParentInterface:

    def parent_function(self):
        ...

    def some_function_that_uses_type_from_another_package(self, some_param: SomeCoolClassType):
        ...

    @property
    def parent_property(self) -> str:
        ...

    @parent_property.setter
    def parent_property(self, value: str) -> None:
        ...


