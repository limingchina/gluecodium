

import typing

class ParentNarrowOne:

    def parent_function_one(self):
        ...

    @property
    def parent_property_one(self) -> str:
        ...

    @parent_property_one.setter
    def parent_property_one(self, value: str) -> None:
        ...

