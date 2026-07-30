

import typing

class ParentClass:

    def parent_fun(self):
        ...

    @property
    def parent_property(self) -> str:
        ...

    @parent_property.setter
    def parent_property(self, value: str) -> None:
        ...

