

from enum import Enum
import typing
from typing import Optional

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
