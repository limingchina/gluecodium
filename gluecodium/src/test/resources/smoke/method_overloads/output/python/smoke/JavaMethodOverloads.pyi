

from enum import Enum
import typing
from typing import Optional

class JavaMethodOverloads:

    def one(self, input: str):
        ...

    def two(self, input: list[str]):
        ...
