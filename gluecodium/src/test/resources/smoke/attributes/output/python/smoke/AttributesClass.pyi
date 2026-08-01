

from enum import Enum
import typing

class AttributesClass:

    def very_fun(self, param: str):
        ...

    @property
    def prop(self) -> str:
        ...

    @prop.setter
    def prop(self, value: str) -> None:
        ...

    PI = False


