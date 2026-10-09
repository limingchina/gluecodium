

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsInternal:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, public_field: str) -> None: ...
    @typing.overload
    def __init__(self, internal_field: float) -> None: ...
    @typing.overload
    def __init__(self, internal_field: float, public_field: str) -> None: ...

    public_field: str

    internal_field: float
