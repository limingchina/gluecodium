

from enum import Enum
import typing
from typing import Optional

class CppRefReturnTypeStruct:
    def __init__(self) -> None: ...

    @staticmethod
    def string_ref() -> str:
        ...
