

from smoke.ValidationUtils import ValidationUtils
from enum import Enum
import typing

class StructsWithMethodsInterface:

    class Vector3:
    
        x: float
    
        y: float
    
        z: float
    
        def distance_to(self, other: StructsWithMethodsInterface.Vector3) -> float:
            ...
    
        def add(self, other: StructsWithMethodsInterface.Vector3) -> StructsWithMethodsInterface.Vector3:
            ...
    
        @staticmethod
        def validate(x: float, y: float, z: float) -> bool:
            ...
    
        @typing.overload
        @staticmethod
        def create(input: str) -> StructsWithMethodsInterface.Vector3:
            ...
    
        @typing.overload
        @staticmethod
        def create(other: StructsWithMethodsInterface.Vector3) -> StructsWithMethodsInterface.Vector3:
            ...
    
    
    
    class StructWithStaticMethodsOnly:
    
        @staticmethod
        def do_stuff():
            ...
    
    

