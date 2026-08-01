

from enum import Enum
import typing

class TypeCollection:

    INVALID_STORAGE_ID = 0

    class Point:
    
        x: float
    
        y: float
    
    
    
    class StructHavingAliasFieldDefinedBelow:
    
        field: int
    
    
    
    TypeCollection.Point = TypeCollection.Point
    
    
    
    int = int
    
    

