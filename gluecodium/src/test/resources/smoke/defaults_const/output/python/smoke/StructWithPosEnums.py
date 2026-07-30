

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.SomethingEnum import SomethingEnum


from _native_base import _NativeBase

import generated


class StructWithPosEnums(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructWithPosEnums):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructWithPosEnums(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def first_field(self) -> SomethingEnum:
        return _wrap(self._native.first_field, SomethingEnum)
    @first_field.setter
    def first_field(self, value: SomethingEnum):
      self._native.first_field = _unwrap(value, SomethingEnum)


    @property
    def explicit_field(self) -> SomethingEnum:
        return _wrap(self._native.explicit_field, SomethingEnum)
    @explicit_field.setter
    def explicit_field(self, value: SomethingEnum):
      self._native.explicit_field = _unwrap(value, SomethingEnum)


    @property
    def last_field(self) -> SomethingEnum:
        return _wrap(self._native.last_field, SomethingEnum)
    @last_field.setter
    def last_field(self, value: SomethingEnum):
      self._native.last_field = _unwrap(value, SomethingEnum)


    FIRST_CONSTANT = SomethingEnum.REALLY_FIRST

