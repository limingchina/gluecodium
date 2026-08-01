

from smoke.TypeCollection import TypeCollection
from enum import Enum
import typing

class Structs:

    @staticmethod
    def swap_point_coordinates(input: Structs.Point) -> Structs.Point:
        ...

    @staticmethod
    def return_all_types_struct(input: Structs.AllTypesStruct) -> Structs.AllTypesStruct:
        ...

    @staticmethod
    def create_point(x: float, y: float) -> TypeCollection.Point:
        ...

    @staticmethod
    def modify_all_types_struct(input: TypeCollection.AllTypesStruct) -> TypeCollection.AllTypesStruct:
        ...

    class Point:
    
        x: float
    
        y: float
    
        @staticmethod
        def from_polar(phi: float, r: float) -> Structs.Point:
            """This is some constructor, which constructs Point from polar coordinates."""
            ...
    
    
    
    class Line:
    
        a: Structs.Point
    
        b: Structs.Point
    
    
    
    class AllTypesStruct:
    
        int8_field: int
    
        uint8_field: int
    
        int16_field: int
    
        uint16_field: int
    
        int32_field: int
    
        uint32_field: int
    
        int64_field: int
    
        uint64_field: int
    
        float_field: float
    
        double_field: float
    
        string_field: str
    
        boolean_field: bool
    
        bytes_field: bytes
    
        point_field: Structs.Point
    
    
    
    class NestingImmutableStruct:
    
        struct_field: Structs.AllTypesStruct
    
    
    
    class DoubleNestingImmutableStruct:
    
        nesting_struct_field: Structs.NestingImmutableStruct
    
    
    
    class StructWithArrayOfImmutable:
    
        array_field: list[Structs.AllTypesStruct]
    
    
    
    class ImmutableStructWithCppAccessors:
    
        trivial_int_field: int
    
        trivial_double_field: float
    
        nontrivial_string_field: str
    
        nontrivial_point_field: Structs.Point
    
        nontrivial_optional_point: Optional[Structs.Point]
    
    
    
    class MutableStructWithCppAccessors:
    
        trivial_int_field: int
    
        trivial_double_field: float
    
        nontrivial_string_field: str
    
        nontrivial_point_field: Structs.Point
    
        nontrivial_optional_point: Optional[Structs.Point]
    
    
    
    class FooBar(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    list[Structs.AllTypesStruct] = list[Structs.AllTypesStruct]
    
    

