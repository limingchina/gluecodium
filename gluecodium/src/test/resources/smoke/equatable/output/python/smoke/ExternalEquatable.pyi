

from enum import Enum
import typing
from typing import Optional

class ExternalEquatable:

    class ExternalEquatableStruct:
        def __eq__(self, other: object) -> bool: ...
        __hash__ = None  # type: ignore[assignment]
        def as_key(self) -> _gluecodium_key_736d6f6b652e45787465726e616c457175617461626c652e45787465726e616c457175617461626c65537472756374: ...

        foo_field: str




class _gluecodium_key_736d6f6b652e45787465726e616c457175617461626c652e45787465726e616c457175617461626c65537472756374(ExternalEquatable.ExternalEquatableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
