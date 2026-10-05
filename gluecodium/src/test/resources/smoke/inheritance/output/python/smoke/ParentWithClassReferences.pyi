

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass
from enum import Enum
import typing
from typing import Optional

class ParentWithClassReferences:

    def class_function(self) -> ChildClassFromClass:
        ...

    @property
    def class_property(self) -> ParentClass:
        ...

    @class_property.setter
    def class_property(self, value: ParentClass) -> None:
        ...
