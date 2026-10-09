

from enum import Enum
import typing
from typing import Optional

class SkipOverloads:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dummy: float) -> None: ...

    dummy: float

    def do_foo(self, input: float):
        """"""
        ...
