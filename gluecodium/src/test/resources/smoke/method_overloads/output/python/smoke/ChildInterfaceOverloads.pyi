

from smoke.ParentInterface import ParentInterface
from enum import Enum
import typing
from typing import Optional

class ChildInterfaceOverloads(
    ParentInterface):

    def foo(self, input: str):
        ...

    def bar(self, input: str):
        ...
