

from enum import Enum
import typing
from typing import Optional

class AttributesStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: str) -> None: ...

    field: str

    def very_fun(self, param: str):
        ...


    PI = False
