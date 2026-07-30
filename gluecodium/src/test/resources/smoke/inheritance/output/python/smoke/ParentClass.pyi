

import typing

class ParentClass:

    def root_method(self):
        ...

    @property
    def root_property(self) -> str:
        ...

    @root_property.setter
    def root_property(self, value: str) -> None:
        ...

