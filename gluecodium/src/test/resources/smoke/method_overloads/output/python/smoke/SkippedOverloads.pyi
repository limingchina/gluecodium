

from enum import Enum
import typing
from typing import Optional

class SkippedOverloads:

    @staticmethod
    def make() -> SkippedOverloads:
        ...

    @staticmethod
    def make_for_dart(input: str) -> SkippedOverloads:
        ...
