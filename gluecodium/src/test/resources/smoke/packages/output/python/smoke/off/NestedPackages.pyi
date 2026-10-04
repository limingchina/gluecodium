

from enum import Enum
import typing
from typing import Optional

class NestedPackages:

    @staticmethod
    def basic_method(input: NestedPackages.SomeStruct) -> NestedPackages.SomeStruct:
        ...

    class SomeStruct:

        some_field: str
