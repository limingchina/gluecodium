

from enum import Enum
import typing
from typing import Optional

class ParentWithCustomConstructor:

    @staticmethod
    def create() -> ParentWithCustomConstructor:
        ...
