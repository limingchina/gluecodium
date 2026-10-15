

from enum import Enum
import typing
from typing import Optional

class PublicFieldsNoInit:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, public_field: str) -> None: ...

    public_field: str

    _internal_field: str
