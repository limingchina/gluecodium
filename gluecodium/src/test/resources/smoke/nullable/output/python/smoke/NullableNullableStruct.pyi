

from smoke.NullableSomeEnum import NullableSomeEnum
from smoke.NullableSomeStruct import NullableSomeStruct
from smoke.SomeInterface import SomeInterface
import typing

class NullableNullableStruct:

    string_field: Optional[str]

    bool_field: Optional[bool]

    double_field: Optional[float]

    struct_field: Optional[NullableSomeStruct]

    enum_field: Optional[NullableSomeEnum]

    array_field: Optional[list[str]]

    inline_array_field: Optional[list[str]]

    map_field: Optional[dict[int, str]]

    instance_field: Optional[SomeInterface]

