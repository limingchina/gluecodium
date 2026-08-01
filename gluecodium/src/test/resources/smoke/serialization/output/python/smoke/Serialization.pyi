

from enum import Enum
import typing

class Serialization:

    class SerializableStruct:
    
        bool_field: bool
    
        byte_field: int
    
        short_field: int
    
        int_field: int
    
        long_field: int
    
        float_field: float
    
        double_field: float
    
        string_field: str
    
        struct_field: Serialization.NestedSerializableStruct
    
        byte_buffer_field: bytes
    
        array_field: list[str]
    
        struct_array_field: list[Serialization.NestedSerializableStruct]
    
        map_field: dict[int, str]
    
        set_field: set[str]
    
        enum_set_field: set[Serialization.SomeEnum]
    
        enum_field: Serialization.SomeEnum
    
    
    
    class NestedSerializableStruct:
    
        some_field: str
    
    
    
    class SomeEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    list[Serialization.NestedSerializableStruct] = list[Serialization.NestedSerializableStruct]
    
    
    
    dict[int, str] = dict[int, str]
    
    

