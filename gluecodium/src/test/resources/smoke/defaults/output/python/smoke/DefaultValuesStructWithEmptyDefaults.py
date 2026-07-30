

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.DefaultValuesStructWithDefaults import DefaultValuesStructWithDefaults


from _native_base import _NativeBase

import generated


class DefaultValuesStructWithEmptyDefaults(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesStructWithEmptyDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DefaultValuesStructWithEmptyDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def ints_field(self) -> list[int]:
        return _wrap(self._native.ints_field, list[int])
    @ints_field.setter
    def ints_field(self, value: list[int]):
      self._native.ints_field = _unwrap(value, list[int])


    @property
    def floats_field(self) -> list[float]:
        return _wrap(self._native.floats_field, list[float])
    @floats_field.setter
    def floats_field(self, value: list[float]):
      self._native.floats_field = _unwrap(value, list[float])


    @property
    def map_field(self) -> dict[int, str]:
        return _wrap(self._native.map_field, dict[int, str])
    @map_field.setter
    def map_field(self, value: dict[int, str]):
      self._native.map_field = _unwrap(value, dict[int, str])


    @property
    def struct_field(self) -> DefaultValuesStructWithDefaults:
        return _wrap(self._native.struct_field, DefaultValuesStructWithDefaults)
    @struct_field.setter
    def struct_field(self, value: DefaultValuesStructWithDefaults):
      self._native.struct_field = _unwrap(value, DefaultValuesStructWithDefaults)


    @property
    def set_type_field(self) -> set[str]:
        return _wrap(self._native.set_type_field, set[str])
    @set_type_field.setter
    def set_type_field(self, value: set[str]):
      self._native.set_type_field = _unwrap(value, set[str])


