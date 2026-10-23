

from enum import Enum
import typing
from typing import Optional

class BasicTypes:
    def __init__(self) -> None: ...

    class SomeStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str
