

from enum import Enum
import typing
from typing import Optional

class SwiftExternalCtor:

    field: str

    @staticmethod
    def make(field: str) -> SwiftExternalCtor:
        ...
