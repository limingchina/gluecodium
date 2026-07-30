

from smoke.DefaultValuesStructWithDefaults import DefaultValuesStructWithDefaults
import typing

class DefaultValuesStructWithEmptyDefaults:

    ints_field: list[int]

    floats_field: list[float]

    map_field: dict[int, str]

    struct_field: DefaultValuesStructWithDefaults

    set_type_field: set[str]

