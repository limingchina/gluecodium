

from smoke.FoodType import FoodType
from smoke.StructWithParameters import StructWithParameters

from _native_base import _NativeBase


class FieldConstructorsNullableTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    nullable_field: Optional[StructWithParameters]

