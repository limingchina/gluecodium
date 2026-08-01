

import datetime
from enum import Enum
import typing
from typing import Callable

class OuterStruct:

    field: str

    def do_nothing(self):
        ...

    class InnerStruct:
    
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
    
    
    
    OuterStruct.InnerEnum = OuterStruct.InnerEnum
    
    
    
    InnerLambda = Callable[[], None]
    
    
    
    class InstantiationError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

