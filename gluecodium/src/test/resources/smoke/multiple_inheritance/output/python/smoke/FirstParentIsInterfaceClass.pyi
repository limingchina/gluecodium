

from another.SomeCoolClassType import SomeCoolClassType
from smoke.ParentInterface import ParentInterface
from smoke.ParentNarrowOne import ParentNarrowOne
import typing

class FirstParentIsInterfaceClass(
    ParentInterface,
    ParentNarrowOne):

    def child_function(self):
        ...

    @property
    def child_property(self) -> str:
        ...

    @child_property.setter
    def child_property(self, value: str) -> None:
        ...

