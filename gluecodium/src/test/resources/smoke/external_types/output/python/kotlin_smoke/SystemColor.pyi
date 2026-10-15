

from enum import Enum
import typing
from typing import Optional

class SystemColor:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, red: float, green: float, blue: float, alpha: float) -> None: ...

    red: float

    green: float

    blue: float

    alpha: float
