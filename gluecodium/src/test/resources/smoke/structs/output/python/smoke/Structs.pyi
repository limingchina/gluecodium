

from smoke.TypeCollection import TypeCollection
from enum import Enum
import typing
from typing import Optional

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
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, x: float, y: float) -> None: ...

        x: float

        y: float

        @staticmethod
        def from_polar(phi: float, r: float) -> Structs.Point:
            """This is some constructor, which constructs Point from polar coordinates."""
            ...



    class Line:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, a: Structs.Point, b: Structs.Point) -> None: ...

        a: Structs.Point

        b: Structs.Point



    class AllTypesStruct:
        def __init__(self, int8_field: int, uint8_field: int, int16_field: int, uint16_field: int, int32_field: int, uint32_field: int, int64_field: int, uint64_field: int, float_field: float, double_field: float, string_field: str, boolean_field: bool, bytes_field: bytes, point_field: Structs.Point) -> None: ...

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
        def __init__(self, struct_field: Structs.AllTypesStruct) -> None: ...

        struct_field: Structs.AllTypesStruct



    class DoubleNestingImmutableStruct:
        def __init__(self, nesting_struct_field: Structs.NestingImmutableStruct) -> None: ...

        nesting_struct_field: Structs.NestingImmutableStruct



    class StructWithArrayOfImmutable:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, array_field: list[Structs.AllTypesStruct]) -> None: ...

        array_field: list[Structs.AllTypesStruct]



    class ImmutableStructWithCppAccessors:
        @typing.overload
        def __init__(self, trivial_int_field: int, trivial_double_field: float, nontrivial_string_field: str, nontrivial_point_field: Structs.Point) -> None: ...
        @typing.overload
        def __init__(self, trivial_int_field: int, trivial_double_field: float, nontrivial_string_field: str, nontrivial_point_field: Structs.Point, nontrivial_optional_point: Optional[Structs.Point]) -> None: ...

        trivial_int_field: int

        trivial_double_field: float

        nontrivial_string_field: str

        nontrivial_point_field: Structs.Point

        nontrivial_optional_point: Optional[Structs.Point]



    class MutableStructWithCppAccessors:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, trivial_int_field: int, trivial_double_field: float, nontrivial_string_field: str, nontrivial_point_field: Structs.Point) -> None: ...
        @typing.overload
        def __init__(self, trivial_int_field: int, trivial_double_field: float, nontrivial_string_field: str, nontrivial_point_field: Structs.Point, nontrivial_optional_point: Optional[Structs.Point]) -> None: ...

        trivial_int_field: int

        trivial_double_field: float

        nontrivial_string_field: str

        nontrivial_point_field: Structs.Point

        nontrivial_optional_point: Optional[Structs.Point]



    class FooBar(Enum):

        FOO = 0
        BAR = 1



    ArrayOfImmutable = list[AllTypesStruct]
