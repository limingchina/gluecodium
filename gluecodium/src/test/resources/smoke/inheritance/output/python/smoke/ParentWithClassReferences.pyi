

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass
import typing

class ParentWithClassReferences:

    def class_function(self) -> ChildClassFromClass:
        ...

    @property
    def class_property(self) -> ParentClass:
        ...

    @class_property.setter
    def class_property(self, value: ParentClass) -> None:
        ...

