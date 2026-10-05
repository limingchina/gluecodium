

from enum import Enum
import typing
from typing import Optional

class FieldCustomConstructorsMix:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int) -> None: ...

    string_field: str

    int_field: int

    bool_field: bool

    @staticmethod
    def create_me(int_value: int, dummy: float) -> FieldCustomConstructorsMix:
        ...
