

from smoke.ImmutableStructNoClash import ImmutableStructNoClash
from enum import Enum
import typing
from typing import Optional

class MutableStructImmutableFields:
    @typing.overload
    def __init__(self, struct_field: ImmutableStructNoClash, int_field: int, bool_field: bool) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...

    struct_field: ImmutableStructNoClash

    int_field: int

    bool_field: bool
