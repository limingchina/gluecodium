

from enum import Enum
import typing
from typing import Optional
from typing import Callable

class LambdasDeclarationOrder:

    class SomeStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    SomeCallback = Callable[[SomeStruct], None]
