

from fire.Enum4 import Enum4
from enum import Enum
import typing
from typing import Optional

class EnumWrapper:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, enum_field: Enum4) -> None: ...

    enum_field: Enum4
