

from enum import Enum
import typing

class OrderInStruct:

    struct_field: OrderInStruct.NestedStruct

    enum_field: OrderInStruct.SomeEnum

    class NestedStruct:
    
        some_field: str
    
    
    
    class SomeEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    

