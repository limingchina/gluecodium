

from __future__ import annotations

from smoke.FoodType import FoodType
from smoke.StructWithParameters import StructWithParameters


from _native_base import _NativeBase

import generated


class FieldConstructorsNullableTypes(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], FieldConstructorsNullableTypes):
            super().__init__(args[0])
        else:
            super().__init__(generated.FieldConstructorsNullableTypes(*args))


    @property
    def nullable_field(self):
        """"""
        return self._native.nullable_field

    @nullable_field.setter
    def nullable_field(self, value):
        self._native.nullable_field = value


from enum import Enum


class FoodType(Enum):
    """"""

    VEGETABLES = 0
    FRUITS = 1

