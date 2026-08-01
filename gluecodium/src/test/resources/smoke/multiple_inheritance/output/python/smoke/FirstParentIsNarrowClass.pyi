

from smoke.ParentNarrowOne import ParentNarrowOne
from smoke.ParentNarrowTwo import ParentNarrowTwo
from enum import Enum
import typing

class FirstParentIsNarrowClass(
    ParentNarrowOne,
    ParentNarrowTwo):

    def child_function(self):
        ...

    @property
    def child_property(self) -> str:
        ...

    @child_property.setter
    def child_property(self, value: str) -> None:
        ...


