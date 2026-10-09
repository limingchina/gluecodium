

from enum import Enum
import typing
from typing import Optional

class TimeZone:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, raw_offset: int) -> None: ...

    raw_offset: int
