

from enum import Enum
import typing

class NullableOverloads:

    @typing.overload
    def foo(self, input: str):
        ...

    @typing.overload
    def foo(self, input: Optional[str]):
        ...


