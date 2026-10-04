

from enum import Enum
import typing
from typing import Optional

class DeprecatedFields:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, normal_field1: str, normal_field2: str) -> None: ...
    @typing.overload
    def __init__(self, normal_field1: str, deprecated_field: str, normal_field2: str) -> None: ...

    normal_field1: str

    #:
    deprecated_field: str

    normal_field2: str
