

from smoke.SerializationNestedSerializableStruct import SerializationNestedSerializableStruct
from smoke.SerializationSomeEnum import SerializationSomeEnum
import typing

class SerializationSerializableStruct:

    bool_field: bool

    byte_field: int

    short_field: int

    int_field: int

    long_field: int

    float_field: float

    double_field: float

    string_field: str

    struct_field: SerializationNestedSerializableStruct

    byte_buffer_field: bytes

    array_field: list[str]

    struct_array_field: list[SerializationNestedSerializableStruct]

    map_field: dict[int, str]

    set_field: set[str]

    enum_set_field: set[SerializationSomeEnum]

    enum_field: SerializationSomeEnum

