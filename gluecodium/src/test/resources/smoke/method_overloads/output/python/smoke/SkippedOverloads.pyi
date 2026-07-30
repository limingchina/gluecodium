

import typing

class SkippedOverloads:

    @staticmethod
    def make() -> SkippedOverloads:
        ...

    @staticmethod
    def make_for_dart(input: str) -> SkippedOverloads:
        ...

