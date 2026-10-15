

from enum import Enum
import typing
from typing import Optional

class StructWithKotlinPositionalDefaults:
    """This is an important struct that uses positional default annotation."""
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, first_free_field: str, second_free_field: bool) -> None: ...
    @typing.overload
    def __init__(self, first_init_field: int, first_free_field: str, second_init_field: float, second_free_field: bool, third_init_field: str) -> None: ...

    first_init_field: int

    first_free_field: str

    second_init_field: float

    second_free_field: bool

    third_init_field: str
