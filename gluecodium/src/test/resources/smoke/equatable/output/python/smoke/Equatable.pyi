

from enum import Enum
import typing

class Equatable:

    class EquatableStruct:
        def __eq__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
    
        bool_field: bool
    
        int_field: int
    
        long_field: int
    
        float_field: float
    
        double_field: float
    
        string_field: str
    
        struct_field: Equatable.NestedEquatableStruct
    
        enum_field: Equatable.SomeEnum
    
        array_field: list[str]
    
        map_field: dict[int, str]
    
    
    
    class EquatableNullableStruct:
        def __eq__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
    
        bool_field: Optional[bool]
    
        int_field: Optional[int]
    
        uint_field: Optional[int]
    
        float_field: Optional[float]
    
        string_field: Optional[str]
    
        struct_field: Optional[Equatable.NestedEquatableStruct]
    
        enum_field: Optional[Equatable.SomeEnum]
    
        array_field: Optional[list[str]]
    
        map_field: Optional[dict[int, str]]
    
    
    
    class NestedEquatableStruct:
        def __eq__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
    
        foo_field: str
    
    
    
    class SomeEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    dict[int, str] = dict[int, str]
    
    

