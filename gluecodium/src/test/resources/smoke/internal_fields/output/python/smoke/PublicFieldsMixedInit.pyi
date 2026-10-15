

from enum import Enum
import typing
from typing import Optional

class PublicFieldsMixedInit:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, public_field2: str) -> None: ...
    @typing.overload
    def __init__(self, public_field1: str, public_field2: str) -> None: ...

    public_field1: str

    public_field2: str

    _internal_field: str
