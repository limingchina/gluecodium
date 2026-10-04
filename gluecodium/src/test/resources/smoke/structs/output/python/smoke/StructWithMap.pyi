

from enum import Enum
import typing
from typing import Optional

class StructWithMap:

    field: dict[str, StructWithMap]
