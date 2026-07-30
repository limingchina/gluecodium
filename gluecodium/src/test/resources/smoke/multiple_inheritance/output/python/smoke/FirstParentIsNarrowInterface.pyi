

from smoke.ParentNarrowOne import ParentNarrowOne
from smoke.ParentNarrowTwo import ParentNarrowTwo
import typing

class FirstParentIsNarrowInterface:

    def child_function(self):
        ...

    @property
    def child_property(self) -> str:
        ...

    @child_property.setter
    def child_property(self, value: str) -> None:
        ...

