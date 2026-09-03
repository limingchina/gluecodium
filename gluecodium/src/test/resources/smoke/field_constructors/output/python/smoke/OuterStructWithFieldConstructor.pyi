

from enum import Enum
import typing

class OuterStructWithFieldConstructor:

    outer_struct_field: OuterStructWithFieldConstructor.InnerStructWithDefaults

    class InnerStructWithDefaults:
    
        inner_struct_field: float
    
    

