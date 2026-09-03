

from enum import Enum
import typing

class DeclarationOrder:

    class MainStruct:
    
        struct_field: DeclarationOrder.NestedStruct
    
        type_def_field: int
    
        struct_array_field: list[DeclarationOrder.NestedStruct]
    
        map_field: dict[int, list[DeclarationOrder.NestedStruct]]
    
        enum_field: DeclarationOrder.SomeEnum
    
    
    
    class NestedStruct:
    
        some_field: str
    
    
    
    class SomeEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    SomeTypeDef = int
    
    
    
    ErrorCodeToMessageMap = dict[int, list[NestedStruct]]
    
    
    
    NestedStructArray = list[NestedStruct]
    
    

