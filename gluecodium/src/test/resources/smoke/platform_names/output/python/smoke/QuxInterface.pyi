

from smoke.QuxStruct import QuxStruct
import typing

class QuxInterface:

    def qux_method(self, qux_parameter: str) -> QuxStruct:
        ...

    @staticmethod
    def qux_create(make_parameter: str) -> QuxInterface:
        ...

    @property
    def qux_property(self) -> int:
        ...

    @qux_property.setter
    def qux_property(self, value: int) -> None:
        ...

