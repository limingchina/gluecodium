

from enum import Enum
import typing
from typing import Optional

class Payload:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, error_code: int, message: str) -> None: ...

    error_code: int

    message: str
