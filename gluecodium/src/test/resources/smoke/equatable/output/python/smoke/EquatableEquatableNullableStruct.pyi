

from smoke.EquatableNestedEquatableStruct import EquatableNestedEquatableStruct
from smoke.EquatableSomeEnum import EquatableSomeEnum
import typing

class EquatableEquatableNullableStruct:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    bool_field: Optional[bool]

    int_field: Optional[int]

    uint_field: Optional[int]

    float_field: Optional[float]

    string_field: Optional[str]

    struct_field: Optional[EquatableNestedEquatableStruct]

    enum_field: Optional[EquatableSomeEnum]

    array_field: Optional[list[str]]

    map_field: Optional[dict[int, str]]

