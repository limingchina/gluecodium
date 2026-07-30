

import typing

class SkipOverloadsInDart:

    @staticmethod
    def make() -> SkipOverloadsInDart:
        ...

    @staticmethod
    def make(input: str) -> SkipOverloadsInDart:
        ...

