

from smoke.ParentClass import ParentClass
from smoke.ParentNarrowOne import ParentNarrowOne
from enum import Enum
import typing

class FirstParentIsClassClass(
    ParentClass,
    ParentNarrowOne):

    def child_function(self):
        ...

    @property
    def child_property(self) -> str:
        ...

    @child_property.setter
    def child_property(self, value: str) -> None:
        ...


