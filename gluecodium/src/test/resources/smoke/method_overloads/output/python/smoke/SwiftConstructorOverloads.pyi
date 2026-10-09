

from enum import Enum
import typing
from typing import Optional

class SwiftConstructorOverloads:

    @staticmethod
    def make(input: str) -> SwiftConstructorOverloads:
        ...

    @staticmethod
    def make_do(throughput: str) -> SwiftConstructorOverloads:
        ...
