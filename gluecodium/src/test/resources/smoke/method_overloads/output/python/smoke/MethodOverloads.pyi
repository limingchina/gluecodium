

from enum import Enum
import typing

class MethodOverloads:

    def is_boolean(self, input: bool) -> bool:
        ...

    def is_boolean(self, input: int) -> bool:
        ...

    def is_boolean(self, input: str) -> bool:
        ...

    def is_boolean(self, input: MethodOverloads.Point) -> bool:
        ...

    def is_boolean(self, input1: bool, input2: int, input3: str, input4: MethodOverloads.Point) -> bool:
        ...

    def is_boolean(self, input: list[str]) -> bool:
        ...

    def is_boolean(self, input: list[int]) -> bool:
        ...

    def is_boolean(self) -> bool:
        ...

    def is_float(self, input: str) -> bool:
        ...

    def is_float(self, input: list[int]) -> bool:
        ...

    class Point:
    
        x: float
    
        y: float
    
    
    
    StringArray = list[str]
    
    
    
    IntArray = list[int]
    
    

