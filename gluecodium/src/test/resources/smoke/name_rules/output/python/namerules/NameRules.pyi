

from enum import Enum
import typing

class NameRules:

    @staticmethod
    def create() -> NameRules:
        ...

    def some_method(self, some_argument: NameRules.ExampleStruct) -> float:
        ...

    @property
    def int_property(self) -> int:
        ...

    @int_property.setter
    def int_property(self, value: int) -> None:
        ...

    @property
    def is_boolean_property(self) -> bool:
        ...

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool) -> None:
        ...

    @property
    def struct_property(self) -> NameRules.ExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: NameRules.ExampleStruct) -> None:
        ...

    class ExampleStruct:
    
        value: float
    
        int_value: list[int]
    
    
    
    class ExampleErrorCode(Enum):
    
        NONE = 0
        FATAL = 1
    
    
    
    list[str] = list[str]
    
    
    
    class ExampleError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

