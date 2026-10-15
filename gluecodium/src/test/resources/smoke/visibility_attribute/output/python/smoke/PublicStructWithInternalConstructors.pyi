

from enum import Enum
import typing
from typing import Optional

class PublicStructWithInternalConstructors:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, some_var: int) -> None: ...

    some_var: int

    @staticmethod
    def _make() -> PublicStructWithInternalConstructors:
        ...
