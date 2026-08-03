

from enum import Enum
import typing

class DefaultValues:

    @staticmethod
    def process_struct_with_defaults(input: DefaultValues.StructWithDefaults) -> DefaultValues.StructWithDefaults:
        ...

    class StructWithDefaults:
    
        int_field: int
    
        uint_field: int
    
        float_field: float
    
        double_field: float
    
        bool_field: bool
    
        string_field: str
    
    
    
    class NullableStructWithDefaults:
    
        int_field: Optional[int]
    
        uint_field: Optional[int]
    
        float_field: Optional[float]
    
        bool_field: Optional[bool]
    
        string_field: Optional[str]
    
    
    
    class StructWithSpecialDefaults:
    
        float_nan_field: float
    
        float_infinity_field: float
    
        float_negative_infinity_field: float
    
        double_nan_field: float
    
        double_infinity_field: float
    
        double_negative_infinity_field: float
    
    
    
    class StructWithEmptyDefaults:
    
        ints_field: list[int]
    
        floats_field: list[float]
    
        map_field: dict[int, str]
    
        struct_field: DefaultValues.StructWithDefaults
    
        set_type_field: set[str]
    
    
    
    class StructWithTypedefDefaults:
    
        long_field: int
    
        bool_field: bool
    
        string_field: str
    
    
    
    LongTypedef = int
    
    
    
    BooleanTypedef = bool
    
    
    
    StringTypedef = str
    
    
    
    FloatArray = list[float]
    
    
    
    IdToStringMap = dict[int, str]
    
    
    
    StringSet = set[str]
    
    

