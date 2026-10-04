

from enum import Enum
import typing
from typing import Optional

class ExternalInterface:

    def some_method(self, some_parameter: int):
        ...

    @property
    def some_property(self) -> str:
        ...


    class SomeStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class SomeEnum(Enum):

        SOME_VALUE = 0
