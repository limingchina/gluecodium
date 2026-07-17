

from smoke.FieldConstructorsNullableTypesStructWithParameters import FieldConstructorsNullableTypesStructWithParameters
from smoke.FoodType import FoodType


from _native_base import _NativeBase

import generated


class FieldConstructorsNullableTypes(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], "_native"):
            super().__init__(args[0]._native)
        else:
            super().__init__(generated.FieldConstructorsNullableTypes(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def nullable_field(self):
        """"""
        return Optional[FieldConstructorsNullableTypesStructWithParameters](self._native.nullable_field)
    @nullable_field.setter
    def nullable_field(self, value):
      self._native.nullable_field = getattr(value, "_native", value)


