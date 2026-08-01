

from enum import Enum
import typing

class Structs:

    @staticmethod
    def get_external_struct() -> Structs.ExternalStruct:
        ...

    @staticmethod
    def get_another_external_struct() -> Structs.AnotherExternalStruct:
        ...

    class ExternalStruct:
    
        string_field: str
    
        external_string_field: str
    
        external_array_field: list[int]
    
        external_struct_field: Structs.AnotherExternalStruct
    
    
    
    class AnotherExternalStruct:
    
        int_field: int
    
    

