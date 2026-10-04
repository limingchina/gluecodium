

from smoke.ParentClass import ParentClass
from enum import Enum
import typing
from typing import Optional

class OuterClassWithInheritance(
    ParentClass):

    def foo(self, input: str) -> str:
        ...

    class InnerClass:

        def bar(self, input: str) -> str:
            ...



    class InnerInterface:

        def baz(self, input: str) -> str:
            ...
