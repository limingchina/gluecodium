

from smoke.FieldConstructorsNullableTypesFoodType import FieldConstructorsNullableTypesFoodType
import typing


from _native_base import _NativeBase

import generated


class FieldConstructorsNullableTypesStructWithParameters(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_FieldConstructorsNullableTypesStructWithParameters):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_FieldConstructorsNullableTypesStructWithParameters(*[_unwrap(arg) for arg in args]))


    @property
    def food_type(self) -> FieldConstructorsNullableTypesFoodType:
        """"""
        return _wrap(self._native.food_type, FieldConstructorsNullableTypesFoodType)
    @food_type.setter
    def food_type(self, value: FieldConstructorsNullableTypesFoodType):
      self._native.food_type = _unwrap(value, FieldConstructorsNullableTypesFoodType)


