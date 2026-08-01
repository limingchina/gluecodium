

from smoke.ValidationUtils import ValidationUtils
from enum import Enum
import typing

class StructsWithMethods:

    class Vector:
    
        x: float
    
        y: float
    
        def distance_to(self, other: StructsWithMethods.Vector) -> float:
            ...
    
        def add(self, other: StructsWithMethods.Vector) -> StructsWithMethods.Vector:
            ...
    
        @staticmethod
        def validate(x: float, y: float) -> bool:
            ...
    
        @staticmethod
        def create(x: float, y: float) -> StructsWithMethods.Vector:
            ...
    
        @staticmethod
        def create(other: StructsWithMethods.Vector) -> StructsWithMethods.Vector:
            ...
    
        @staticmethod
        def create(input: int) -> StructsWithMethods.Vector:
            ...
    
    

