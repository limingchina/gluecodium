

from enum import Enum
import typing
from typing import Optional

class AttributesWithDeprecated:
    """"""

    def very_fun(self):
        """"""
        ...

    @property
    def prop(self) -> str:
        """"""
        ...

    @prop.setter
    def prop(self, value: str) -> None:
        ...

    class SomeStruct:

        #:
        field: str



    #:
    PI = False
