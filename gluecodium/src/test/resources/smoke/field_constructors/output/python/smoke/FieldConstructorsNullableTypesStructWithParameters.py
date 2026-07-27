

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.FieldConstructorsNullableTypesFoodType import FieldConstructorsNullableTypesFoodType


from _native_base import _NativeBase

import generated


class FieldConstructorsNullableTypesStructWithParameters(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_FieldConstructorsNullableTypesStructWithParameters):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_FieldConstructorsNullableTypesStructWithParameters(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def food_type(self) -> FieldConstructorsNullableTypesFoodType:
        """"""
        return _wrap(self._native.food_type, FieldConstructorsNullableTypesFoodType)
    @food_type.setter
    def food_type(self, value: FieldConstructorsNullableTypesFoodType):
      self._native.food_type = _unwrap(value, FieldConstructorsNullableTypesFoodType)


