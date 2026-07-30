

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.EnumOptionSet import EnumOptionSet


from _native_base import _NativeBase

import generated


class UseEnumOptionSet(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_UseEnumOptionSet):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_UseEnumOptionSet(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def set_field(self) -> set[EnumOptionSet]:
        return _wrap(self._native.set_field, set[EnumOptionSet])
    @set_field.setter
    def set_field(self, value: set[EnumOptionSet]):
      self._native.set_field = _unwrap(value, set[EnumOptionSet])


    @property
    def set_field_empty(self) -> set[EnumOptionSet]:
        return _wrap(self._native.set_field_empty, set[EnumOptionSet])
    @set_field_empty.setter
    def set_field_empty(self, value: set[EnumOptionSet]):
      self._native.set_field_empty = _unwrap(value, set[EnumOptionSet])


    @property
    def set_field_value(self) -> set[EnumOptionSet]:
        return _wrap(self._native.set_field_value, set[EnumOptionSet])
    @set_field_value.setter
    def set_field_value(self, value: set[EnumOptionSet]):
      self._native.set_field_value = _unwrap(value, set[EnumOptionSet])


    @staticmethod
    def round_trip(input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        return _wrap(generated.smoke_UseEnumOptionSet.round_trip(_unwrap(input, set[EnumOptionSet])), set[EnumOptionSet])

