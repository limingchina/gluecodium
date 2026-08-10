

from smoke.ParentClass import ParentClass
from enum import Enum
import typing

class ChildClassFromClassOverloads(
    ParentClass):

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


