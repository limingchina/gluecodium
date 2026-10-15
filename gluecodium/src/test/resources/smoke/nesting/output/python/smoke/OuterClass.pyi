

from enum import Enum
import typing
from typing import Optional

class OuterClass:

    def foo(self, input: str) -> str:
        ...

    class InnerClass:

        def foo(self, input: str) -> str:
            ...



    class InnerInterface:

        def foo(self, input: str) -> str:
            ...
