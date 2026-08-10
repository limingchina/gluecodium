

from enum import Enum
import typing

class Constructors:

    @typing.overload
    @staticmethod
    def create() -> Constructors:
        ...

    @typing.overload
    @staticmethod
    def create(other: Constructors) -> Constructors:
        ...

    @typing.overload
    @staticmethod
    def create(foo: str, bar: int) -> Constructors:
        ...

    @typing.overload
    @staticmethod
    def create(input: str) -> Constructors:
        ...

    @typing.overload
    @staticmethod
    def create(input: list[float]) -> Constructors:
        ...

    @typing.overload
    @staticmethod
    def create(input: int) -> Constructors:
        ...

    class ErrorEnum(Enum):
    
        NONE = 0
        CRASHED = 1
    
    
    
    class ConstructorExplodedError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

