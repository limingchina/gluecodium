

from smoke.ParentInterface import ParentInterface
from enum import Enum
import typing

class ChildClassFromInterfaceOverloads(
    ParentInterface):

    @typing.overload
    def foo(self, input: str):
        ...

    @typing.overload
    def foo(self, input: float):
        ...

    @typing.overload
    def bar(self, input: str):
        ...

    @typing.overload
    def bar(self, input: float):
        ...


