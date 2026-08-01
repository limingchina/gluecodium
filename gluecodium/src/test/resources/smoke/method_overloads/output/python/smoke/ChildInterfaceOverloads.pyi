

from smoke.ParentInterface import ParentInterface
from enum import Enum
import typing

class ChildInterfaceOverloads:

    def foo(self, input: str):
        ...

    def bar(self, input: str):
        ...


