

from enum import Enum
import typing
from typing import Optional

class StructWithConstMethod:

    string_field: str

    def double_const(self) -> float:
        ...
