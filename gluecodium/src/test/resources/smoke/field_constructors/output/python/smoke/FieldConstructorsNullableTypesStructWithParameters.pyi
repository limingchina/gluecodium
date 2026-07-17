

from smoke.FoodType import FoodType


from _native_base import _NativeBase

import generated


class FieldConstructorsNullableTypesStructWithParameters(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.FieldConstructorsNullableTypesStructWithParameters):
            super().__init__(args[0])
        else:
            super().__init__(generated.FieldConstructorsNullableTypesStructWithParameters(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def food_type(self) -> FoodType:
        """"""
        return FoodType(self._native.food_type)
    @food_type.setter
    def food_type(self, value: FoodType):
      self._native.food_type = getattr(value, "_native", value)


