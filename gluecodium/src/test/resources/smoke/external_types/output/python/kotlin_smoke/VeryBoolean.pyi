

from enum import Enum
import typing
from typing import Optional

class VeryBoolean:

    value: bool

    @staticmethod
    def make(value: bool) -> VeryBoolean:
        ...
