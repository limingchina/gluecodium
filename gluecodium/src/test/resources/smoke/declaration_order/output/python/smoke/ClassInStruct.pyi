

from enum import Enum
import typing
from typing import Optional
from typing import Callable

class ClassInStruct:

    class FooChecker:
        ...



    SomeLambda = Callable[[FooChecker], None]
