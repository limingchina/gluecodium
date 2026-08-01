

from smoke.ParentInterface import ParentInterface
from enum import Enum
import typing

class ChildClassFromInterfaceOverloads(
    ParentInterface):

    def foo(self, input: str):
        ...

    def foo(self, input: float):
        ...

    def bar(self, input: str):
        ...

    def bar(self, input: float):
        ...


