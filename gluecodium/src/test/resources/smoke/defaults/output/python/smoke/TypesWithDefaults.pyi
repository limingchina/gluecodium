

from enum import Enum
import typing

class TypesWithDefaults:

    class StructWithDefaults:
    
        int_field: int
    
        uint_field: int
    
        float_field: float
    
        double_field: float
    
        bool_field: bool
    
        string_field: str
    
    
    
    class ImmutableStructWithDefaults:
    
        int_field: int
    
        uint_field: int
    
        float_field: float
    
        double_field: float
    
        bool_field: bool
    
        string_field: str
    
    
    
    class ImmutableStructWithCollections:
    
        nullable_list_field: Optional[list[int]]
    
        empty_list_field: list[int]
    
        values_list_field: list[int]
    
        nullable_map_field: Optional[dict[int, str]]
    
        empty_map_field: dict[int, str]
    
        values_map_field: dict[int, str]
    
        nullable_set_field: Optional[set[str]]
    
        empty_set_field: set[str]
    
        values_set_field: set[str]
    
    
    
    class ImmutableStructWithFieldConstructorAndCollections:
    
        nullable_list_field: Optional[list[int]]
    
        empty_list_field: list[int]
    
        values_list_field: list[int]
    
        nullable_map_field: Optional[dict[int, str]]
    
        empty_map_field: dict[int, str]
    
        values_map_field: dict[int, str]
    
        nullable_set_field: Optional[set[str]]
    
        empty_set_field: set[str]
    
        values_set_field: set[str]
    
        some_field: int
    
        another_field: int
    
    
    
    class SomeImmutableStructWithDefaults:
    
        int_field: int
    
    
    
    class ImmutableStructWithFieldUsingImmutableStruct:
    
        some_field1: TypesWithDefaults.SomeImmutableStructWithDefaults
    
        some_field2: TypesWithDefaults.ImmutableStructWithCollections
    
    
    
    class ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct:
    
        some_field1: TypesWithDefaults.SomeImmutableStructWithDefaults
    
        some_field2: TypesWithDefaults.ImmutableStructWithCollections
    
        some_field: int
    
        another_field: int
    
    
    
    class ImmutableStructWithNullableFieldUsingImmutableStruct:
    
        some_field1: Optional[TypesWithDefaults.SomeImmutableStructWithDefaults]
    
        some_field2: Optional[TypesWithDefaults.ImmutableStructWithCollections]
    
    
    
    class ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct:
    
        some_field1: Optional[TypesWithDefaults.SomeImmutableStructWithDefaults]
    
        some_field2: Optional[TypesWithDefaults.ImmutableStructWithCollections]
    
        some_field: int
    
        another_field: int
    
    

