

from smoke.ParentClass import ParentClass
from enum import Enum
import typing

class ChildClassFromClassOverloads(
    ParentClass):

    def foo(self, input: str):
        ...

    def foo(self, input: float):
        ...

    def bar(self, input: str):
        ...

    def bar(self, input: float):
        ...


