

from smoke.ImmutableDefaultCtor import ImmutableDefaultCtor
from enum import Enum
import typing
from typing import Optional

class MutableStructImmutableFieldsDefault:
    def __init__(self) -> None: ...

    struct_field: ImmutableDefaultCtor

    int_field: int

    bool_field: bool
