

from enum import Enum
import typing
from typing import Optional

class JavaExternalCtor:

    field: str

    @staticmethod
    def make(field: str) -> JavaExternalCtor:
        ...
