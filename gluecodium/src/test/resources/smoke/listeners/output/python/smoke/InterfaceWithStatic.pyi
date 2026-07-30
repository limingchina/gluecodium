

import typing

class InterfaceWithStatic:

    def regular_function(self) -> str:
        ...

    @staticmethod
    def static_function() -> str:
        ...

    @property
    def regular_property(self) -> str:
        ...

    @regular_property.setter
    def regular_property(self, value: str) -> None:
        ...

    @property
    def static_property(self) -> str:
        ...

    @static_property.setter
    def static_property(self, value: str) -> None:
        ...

