

from enum import Enum
import typing

class ExternalClass:

    @staticmethod
    def create() -> ExternalClass:
        ...

    class InternalOne:
    
        @typing.overload
        @staticmethod
        def create() -> ExternalClass.InternalOne:
            ...
    
        @typing.overload
        @staticmethod
        def create(value: int) -> ExternalClass.InternalOne:
            ...
    
    
    
    class InternalTwo:
    
        @staticmethod
        def create() -> ExternalClass.InternalTwo:
            ...
    
    
    
    class ErrorEnum(Enum):
    
        NONE = 0
        CRASHED = 1
    
    
    
    class ConstructorExplodedError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

