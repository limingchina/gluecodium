

from enum import Enum
import typing
from typing import Optional

class MutableStructNoClash:
    def __init__(self) -> None: ...

    string_field: str

    int_field: int

    bool_field: bool
