

from fire.SomeStruct import SomeStruct
from enum import Enum
import typing
from typing import Optional

class ConstantDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field1: SomeStruct, field2: SomeStruct) -> None: ...

    field1: SomeStruct

    field2: SomeStruct
