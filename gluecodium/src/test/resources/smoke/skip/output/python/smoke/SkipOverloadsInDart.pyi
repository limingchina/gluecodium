

from enum import Enum
import typing

class SkipOverloadsInDart:

    @typing.overload
    @staticmethod
    def make() -> SkipOverloadsInDart:
        ...

    @typing.overload
    @staticmethod
    def make(input: str) -> SkipOverloadsInDart:
        ...


