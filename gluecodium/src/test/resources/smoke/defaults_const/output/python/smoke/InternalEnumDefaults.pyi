

from smoke.FooBarEnum import FooBarEnum
from enum import Enum
import typing
from typing import Optional

class InternalEnumDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, public_field: FooBarEnum, public_list_field: list[FooBarEnum]) -> None: ...

    public_field: FooBarEnum

    public_list_field: list[FooBarEnum]

    _internal_field: FooBarEnum

    _internal_list_field: list[FooBarEnum]
