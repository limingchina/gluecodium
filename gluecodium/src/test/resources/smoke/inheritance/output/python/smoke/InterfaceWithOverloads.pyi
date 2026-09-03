

from enum import Enum
import typing

class InterfaceWithOverloads:

    @typing.overload
    def parent_method(self):
        ...

    @typing.overload
    def parent_method(self, input: str):
        ...


