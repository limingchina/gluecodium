

from enum import Enum
import typing
from typing import Optional

class ParentNarrowTwo:

    def parent_function_two(self):
        ...

    @property
    def parent_property_two(self) -> str:
        ...

    @parent_property_two.setter
    def parent_property_two(self, value: str) -> None:
        ...
