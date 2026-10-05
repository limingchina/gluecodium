

from enum import Enum
import typing
from typing import Optional

class ExternalMarkedAsSerializable:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: int) -> None: ...

    field: int
