

from enum import Enum
import typing
from typing import Optional
from typing import Callable

class ClassInStruct:
    def __init__(self) -> None: ...

    class FooChecker:
        ...



    SomeLambda = Callable[[FooChecker], None]
