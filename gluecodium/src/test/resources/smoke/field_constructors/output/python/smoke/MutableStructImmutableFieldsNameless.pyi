

from smoke.ImmutableNamelessCtor import ImmutableNamelessCtor
from enum import Enum
import typing
from typing import Optional

class MutableStructImmutableFieldsNameless:
    def __init__(self) -> None: ...

    struct_field: ImmutableNamelessCtor

    int_field: int

    bool_field: bool
