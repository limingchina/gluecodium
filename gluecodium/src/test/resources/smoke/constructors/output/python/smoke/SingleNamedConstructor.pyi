

from enum import Enum
import typing
from typing import Optional

class SingleNamedConstructor:

    @staticmethod
    def create() -> SingleNamedConstructor:
        ...
