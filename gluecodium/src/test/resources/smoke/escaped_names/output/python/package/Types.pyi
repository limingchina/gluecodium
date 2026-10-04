

from enum import Enum
import typing
from typing import Optional

class Types:

    class Struct:

        null: Types.Enum



    class Enum(Enum):

        NA_N = 0



    class ExceptionError(Exception):
        message: str

        def __init__(self, message: str) -> None: ...



    ULong = list[Struct]



    CONST = Enum.NA_N
