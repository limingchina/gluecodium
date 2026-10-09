

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
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, field: str) -> None: ...

        #:
        field: str



    #:
    PI = False
