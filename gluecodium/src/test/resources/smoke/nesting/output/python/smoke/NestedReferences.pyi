

from enum import Enum
import typing
from typing import Optional

class NestedReferences:

    def inside_out(self, struct1: NestedReferences.NestedReferences, struct2: NestedReferences.NestedReferences) -> NestedReferences:
        ...

    class NestedReferences:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, string_field: str) -> None: ...

        string_field: str
