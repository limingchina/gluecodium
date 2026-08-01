

from enum import Enum
import typing

class OrderInStructWithFunctions:

    some_field: str

    def do_stuff(self, struct_foo: OrderInStructWithFunctions.NestedStruct) -> OrderInStructWithFunctions.SomeEnum:
        ...

    class NestedStruct:
    
        some_field: str
    
    
    
    class SomeEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    

