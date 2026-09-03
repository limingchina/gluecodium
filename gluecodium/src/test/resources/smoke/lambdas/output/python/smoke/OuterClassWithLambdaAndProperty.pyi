

from enum import Enum
import typing
from typing import Callable

class OuterClassWithLambdaAndProperty:

    @property
    def some_integer(self) -> int:
        ...

    @some_integer.setter
    def some_integer(self, value: int) -> None:
        ...

    @property
    def another_integer(self) -> int:
        ...

    @another_integer.setter
    def another_integer(self, value: int) -> None:
        ...

    SomeInternalLambda = Callable[[int], int]
    
    

