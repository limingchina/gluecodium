

from enum import Enum
import typing
from typing import Optional

class ClassWithStructWithSkipLambdaInPlatform:

    class SkipLambdaInPlatform:
        def __init__(self) -> None: ...

        int_field: int
