

import typing

class DartColor:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    red: float

    green: float

    blue: float

    alpha: float

