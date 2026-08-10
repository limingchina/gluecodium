

from enum import Enum
import typing

class ParentInterface:

    @typing.overload
    def foo(self):
        ...

    @typing.overload
    def foo(self, input: int):
        ...

    def bar(self):
        ...

    def baz(self):
        ...


