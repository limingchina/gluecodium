

from enum import Enum
import typing

class ExternalInterface:

    def some_method(self, some_parameter: int):
        ...

    @property
    def some_property(self) -> str:
        ...


    class SomeStruct:
    
        some_field: str
    
    
    
    class SomeEnum(Enum):
    
        SOME_VALUE = 0
    
    

