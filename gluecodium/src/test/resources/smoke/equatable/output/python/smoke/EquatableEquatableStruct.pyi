

from smoke.EquatableNestedEquatableStruct import EquatableNestedEquatableStruct
from smoke.EquatableSomeEnum import EquatableSomeEnum
import typing

class EquatableEquatableStruct:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    bool_field: bool

    int_field: int

    long_field: int

    float_field: float

    double_field: float

    string_field: str

    struct_field: EquatableNestedEquatableStruct

    enum_field: EquatableSomeEnum

    array_field: list[str]

    map_field: dict[int, str]

