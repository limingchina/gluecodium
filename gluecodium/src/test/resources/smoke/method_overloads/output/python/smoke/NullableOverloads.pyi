

from enum import Enum
import typing

class NullableOverloads:

    def foo(self, input: str):
        ...

    def foo(self, input: Optional[str]):
        ...


