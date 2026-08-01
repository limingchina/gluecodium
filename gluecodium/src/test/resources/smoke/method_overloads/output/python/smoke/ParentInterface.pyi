

from enum import Enum
import typing

class ParentInterface:

    def foo(self):
        ...

    def foo(self, input: int):
        ...

    def bar(self):
        ...

    def baz(self):
        ...


