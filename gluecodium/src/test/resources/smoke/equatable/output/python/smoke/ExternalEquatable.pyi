

from enum import Enum
import typing
from typing import Optional

class ExternalEquatable:
    def __init__(self) -> None: ...

    class ExternalEquatableStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, foo_field: str) -> None: ...
        def __eq__(self, other: object) -> bool: ...
        __hash__ = None  # type: ignore[assignment]
        def as_key(self) -> _gluecodium_key_736d6f6b652e45787465726e616c457175617461626c652e45787465726e616c457175617461626c65537472756374: ...

        foo_field: str




class _gluecodium_key_736d6f6b652e45787465726e616c457175617461626c652e45787465726e616c457175617461626c65537472756374(ExternalEquatable.ExternalEquatableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
