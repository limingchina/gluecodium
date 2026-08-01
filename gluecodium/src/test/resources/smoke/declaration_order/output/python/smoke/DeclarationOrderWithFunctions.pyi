

from enum import Enum
import typing

class DeclarationOrderWithFunctions:

    class MainStructWithFunctions:
    
        struct_field: DeclarationOrderWithFunctions.FieldStruct
    
        def with_parameter(self, input: DeclarationOrderWithFunctions.ParameterStruct):
            ...
    
        def with_return(self) -> DeclarationOrderWithFunctions.ReturnStruct:
            ...
    
        def with_thrown(self):
            ...
    
    
    
    class FieldStruct:
    
        some_field: str
    
    
    
    class ParameterStruct:
    
        some_field: str
    
    
    
    class ReturnStruct:
    
        some_field: str
    
    
    
    class ThrownStruct:
    
        some_field: str
    
    
    
    class FooBarError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

