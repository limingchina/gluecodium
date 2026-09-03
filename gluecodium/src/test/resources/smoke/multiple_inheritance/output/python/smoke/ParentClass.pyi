

from enum import Enum
import typing

class ParentClass:

    def parent_function(self):
        ...

    @property
    def parent_property(self) -> str:
        ...

    @parent_property.setter
    def parent_property(self, value: str) -> None:
        ...


