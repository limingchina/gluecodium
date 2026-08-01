

from enum import Enum
import typing

class OrderInClass:

    class MainStruct:
    
        struct_field: OrderInClass.NestedStruct
    
        type_def_field: int
    
        struct_array_field: list[OrderInClass.NestedStruct]
    
        map_field: dict[int, list[OrderInClass.NestedStruct]]
    
        enum_field: OrderInClass.SomeEnum
    
    
    
    class NestedStruct:
    
        some_field: str
    
    
    
    class SomeEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    int = int
    
    
    
    dict[int, list[OrderInClass.NestedStruct]] = dict[int, list[OrderInClass.NestedStruct]]
    
    
    
    list[OrderInClass.NestedStruct] = list[OrderInClass.NestedStruct]
    
    

