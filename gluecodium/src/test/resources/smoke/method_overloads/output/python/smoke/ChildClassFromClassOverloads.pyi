

from smoke.ParentClass import ParentClass
from enum import Enum
import typing
from typing import Optional

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
