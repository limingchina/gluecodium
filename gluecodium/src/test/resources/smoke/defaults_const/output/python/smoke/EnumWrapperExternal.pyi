

from fire.ExternalEnum4 import ExternalEnum4
from enum import Enum
import typing
from typing import Optional

class EnumWrapperExternal:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, enum_field: ExternalEnum4) -> None: ...

    enum_field: ExternalEnum4
