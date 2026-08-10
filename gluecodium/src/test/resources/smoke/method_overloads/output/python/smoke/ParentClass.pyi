

from enum import Enum
import typing

class ParentClass:

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


