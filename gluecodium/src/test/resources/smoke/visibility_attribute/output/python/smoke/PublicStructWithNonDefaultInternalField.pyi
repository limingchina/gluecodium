

from enum import Enum
import typing
from typing import Optional

class PublicStructWithNonDefaultInternalField:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, public_field: bool) -> None: ...
    @typing.overload
    def __init__(self, defaulted_field: int, public_field: bool) -> None: ...

    defaulted_field: int

    _internal_field: str

    public_field: bool
