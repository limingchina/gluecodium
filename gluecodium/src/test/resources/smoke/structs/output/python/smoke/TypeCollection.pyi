

from enum import Enum
import typing

class TypeCollection:

    class Point:
    
        x: float
    
        y: float
    
    
    
    class Line:
    
        a: TypeCollection.Point
    
        b: TypeCollection.Point
    
    
    
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
    
        point_field: TypeCollection.Point
    
    
    
    PointTypedef = Point
    
    

