

from smoke.StructsPoint import StructsPoint
import typing

class StructsImmutableStructWithCppAccessors:

    trivial_int_field: int

    trivial_double_field: float

    nontrivial_string_field: str

    nontrivial_point_field: StructsPoint

    nontrivial_optional_point: Optional[StructsPoint]

