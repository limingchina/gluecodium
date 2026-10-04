

from enum import Enum
import typing
from typing import Optional

class InterfaceWithOverloads:

    @typing.overload
    def parent_method(self):
        ...

    @typing.overload
    def parent_method(self, input: str):
        ...
