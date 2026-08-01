

from enum import Enum
import typing

class StructConstants:

    STRUCT_CONSTANT = {"bar Buzz", 1.41}

    NESTING_STRUCT_CONSTANT = {{"nonsense", -2.82}}

    class SomeStruct:
    
        string_field: str
    
        float_field: float
    
    
    
    class NestingStruct:
    
        struct_field: StructConstants.SomeStruct
    
    

