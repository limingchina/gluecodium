

from enum import Enum
import typing
from typing import Optional

class NullableOverloads:

    @typing.overload
    def foo(self, input: str):
        ...

    @typing.overload
    def foo(self, input: Optional[str]):
        ...
