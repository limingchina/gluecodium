

from enum import Enum
import typing

class Types:

    CONST = Enum.NA_N

    class Struct:
    
        null: Types.Enum
    
    
    
    class Enum(Enum):
    
        NA_N = 0
    
    
    
    list[Types.Struct] = list[Types.Struct]
    
    
    
    class ExceptionError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

