

from enum import Enum
import typing
from typing import Optional

class AttributesInterface:

    def very_fun(self, param: str):
        ...

    @property
    def prop(self) -> str:
        ...

    @prop.setter
    def prop(self, value: str) -> None:
        ...


    PI = False
