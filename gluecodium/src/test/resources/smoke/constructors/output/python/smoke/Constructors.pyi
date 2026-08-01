

from enum import Enum
import typing

class Constructors:

    @staticmethod
    def create() -> Constructors:
        ...

    @staticmethod
    def create(other: Constructors) -> Constructors:
        ...

    @staticmethod
    def create(foo: str, bar: int) -> Constructors:
        ...

    @staticmethod
    def create(input: str) -> Constructors:
        ...

    @staticmethod
    def create(input: list[float]) -> Constructors:
        ...

    @staticmethod
    def create(input: int) -> Constructors:
        ...

    class ErrorEnum(Enum):
    
        NONE = 0
        CRASHED = 1
    
    
    
    class ConstructorExplodedError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

