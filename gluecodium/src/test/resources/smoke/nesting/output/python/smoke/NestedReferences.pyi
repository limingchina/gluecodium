

from enum import Enum
import typing
from typing import Optional

class NestedReferences:

    def inside_out(self, struct1: NestedReferences.NestedReferences, struct2: NestedReferences.NestedReferences) -> NestedReferences:
        ...

    class NestedReferences:

        string_field: str
