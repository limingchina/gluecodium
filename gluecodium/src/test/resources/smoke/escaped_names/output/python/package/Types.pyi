

from enum import Enum
import typing
from typing import Optional

class Types:
    def __init__(self) -> None: ...

    class Struct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, null: Types.Enum) -> None: ...

        null: Types.Enum



    class Enum(Enum):

        NA_N = 0



    class ExceptionError(Exception):
        message: str

        def __init__(self, message: str) -> None: ...



    ULong = list[Struct]



    CONST = Enum.NA_N
