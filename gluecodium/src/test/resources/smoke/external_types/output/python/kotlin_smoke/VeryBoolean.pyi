

from enum import Enum
import typing
from typing import Optional

class VeryBoolean:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, value: bool) -> None: ...

    value: bool

    @staticmethod
    def make(value: bool) -> VeryBoolean:
        ...
