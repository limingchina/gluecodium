

import datetime
from enum import Enum
import typing
from typing import Optional
from typing import Callable

class OuterStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: str) -> None: ...

    field: str

    def do_nothing(self):
        ...

    class InnerStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, other_field: list[datetime.datetime]) -> None: ...

        other_field: list[datetime.datetime]

        def do_something(self):
            ...



    class InnerClass:

        def foo_bar(self) -> set[str]:
            ...



    class Builder:

        @staticmethod
        def create() -> OuterStruct.Builder:
            ...

        def field(self, value: str) -> OuterStruct.Builder:
            ...

        def build(self) -> OuterStruct:
            ...



    class InnerInterface:

        def bar_baz(self) -> dict[str, bytes]:
            ...



    class InnerEnum(Enum):

        FOO = 0
        BAR = 1



    class InstantiationError(Exception):
        message: str

        def __init__(self, message: str) -> None: ...



    TypeAlias = InnerEnum



    InnerLambda = Callable[[], None]
