

from fire.AmbiguousEnum import AmbiguousEnum
from fire.SomeStruct import SomeStruct
from enum import Enum
import typing
from typing import Optional

class AmbiguousDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field1: AmbiguousEnum, field2: SomeStruct) -> None: ...

    field1: AmbiguousEnum

    field2: SomeStruct
