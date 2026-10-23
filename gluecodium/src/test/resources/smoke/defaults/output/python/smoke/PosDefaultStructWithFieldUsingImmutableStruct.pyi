

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults
from enum import Enum
import typing
from typing import Optional

class PosDefaultStructWithFieldUsingImmutableStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, some_field1: ImmutableStructWithDefaults) -> None: ...

    some_field1: ImmutableStructWithDefaults
