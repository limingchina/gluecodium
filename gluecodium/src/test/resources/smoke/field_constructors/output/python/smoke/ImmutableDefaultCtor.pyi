

from enum import Enum
import typing
from typing import Optional

class ImmutableDefaultCtor:
    def __init__(self) -> None: ...

    string_field: str
