

from enum import Enum
import typing
from typing import Optional

class SkipOverloadsInDart:

    @typing.overload
    @staticmethod
    def make() -> SkipOverloadsInDart:
        ...

    @typing.overload
    @staticmethod
    def make(input: str) -> SkipOverloadsInDart:
        ...
