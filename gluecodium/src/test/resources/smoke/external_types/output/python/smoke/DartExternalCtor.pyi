

from enum import Enum
import typing
from typing import Optional

class DartExternalCtor:

    field: str

    @staticmethod
    def make(field: str) -> DartExternalCtor:
        ...
