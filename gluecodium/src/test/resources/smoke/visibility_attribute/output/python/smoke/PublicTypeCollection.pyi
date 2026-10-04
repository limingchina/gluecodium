

from enum import Enum
import typing
from typing import Optional

class PublicTypeCollection:
    def __init__(self) -> None: ...

    class _InternalStruct:
        def __init__(self) -> None: ...

        _string_field: str

        def foo_bar(self):
            ...
