

from enum import Enum
import typing

class FieldCustomConstructorsMix:

    string_field: str

    int_field: int

    bool_field: bool

    @staticmethod
    def create_me(int_value: int, dummy: float) -> FieldCustomConstructorsMix:
        ...


