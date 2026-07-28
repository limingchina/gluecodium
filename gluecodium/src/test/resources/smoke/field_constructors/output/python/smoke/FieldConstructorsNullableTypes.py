

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.FieldConstructorsNullableTypesFoodType import FieldConstructorsNullableTypesFoodType
from smoke.FieldConstructorsNullableTypesStructWithParameters import FieldConstructorsNullableTypesStructWithParameters


from _native_base import _NativeBase

import generated


class FieldConstructorsNullableTypes(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_FieldConstructorsNullableTypes):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_FieldConstructorsNullableTypes(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def nullable_field(self):
        """"""
        return _wrap(self._native.nullable_field, Optional[FieldConstructorsNullableTypesStructWithParameters])
    @nullable_field.setter
    def nullable_field(self, value):
      self._native.nullable_field = _unwrap(value, Optional[FieldConstructorsNullableTypesStructWithParameters])


