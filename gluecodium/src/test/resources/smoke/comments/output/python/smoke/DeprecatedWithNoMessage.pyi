

from enum import Enum
import typing
from typing import Optional

class DeprecatedWithNoMessage:
    """"""
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: str) -> None: ...

    field: str
