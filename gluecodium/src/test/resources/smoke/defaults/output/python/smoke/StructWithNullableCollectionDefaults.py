

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithNullableCollectionDefaults(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructWithNullableCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructWithNullableCollectionDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def nullable_list_field(self):
        return _wrap(self._native.nullable_list_field, Optional[list[str]])
    @nullable_list_field.setter
    def nullable_list_field(self, value):
      self._native.nullable_list_field = _unwrap(value, Optional[list[str]])


    @property
    def nullable_map_field(self):
        return _wrap(self._native.nullable_map_field, Optional[dict[str, str]])
    @nullable_map_field.setter
    def nullable_map_field(self, value):
      self._native.nullable_map_field = _unwrap(value, Optional[dict[str, str]])


    @property
    def nullable_set_field(self):
        return _wrap(self._native.nullable_set_field, Optional[set[str]])
    @nullable_set_field.setter
    def nullable_set_field(self, value):
      self._native.nullable_set_field = _unwrap(value, Optional[set[str]])


