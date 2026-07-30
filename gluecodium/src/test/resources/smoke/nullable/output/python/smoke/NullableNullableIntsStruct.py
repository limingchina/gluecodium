

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class NullableNullableIntsStruct(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NullableNullableIntsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_NullableNullableIntsStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def int8_field(self):
        return _wrap(self._native.int8_field, Optional[int])
    @int8_field.setter
    def int8_field(self, value):
      self._native.int8_field = _unwrap(value, Optional[int])


    @property
    def int16_field(self):
        return _wrap(self._native.int16_field, Optional[int])
    @int16_field.setter
    def int16_field(self, value):
      self._native.int16_field = _unwrap(value, Optional[int])


    @property
    def int32_field(self):
        return _wrap(self._native.int32_field, Optional[int])
    @int32_field.setter
    def int32_field(self, value):
      self._native.int32_field = _unwrap(value, Optional[int])


    @property
    def int64_field(self):
        return _wrap(self._native.int64_field, Optional[int])
    @int64_field.setter
    def int64_field(self, value):
      self._native.int64_field = _unwrap(value, Optional[int])


    @property
    def uint8_field(self):
        return _wrap(self._native.uint8_field, Optional[int])
    @uint8_field.setter
    def uint8_field(self, value):
      self._native.uint8_field = _unwrap(value, Optional[int])


    @property
    def uint16_field(self):
        return _wrap(self._native.uint16_field, Optional[int])
    @uint16_field.setter
    def uint16_field(self, value):
      self._native.uint16_field = _unwrap(value, Optional[int])


    @property
    def uint32_field(self):
        return _wrap(self._native.uint32_field, Optional[int])
    @uint32_field.setter
    def uint32_field(self, value):
      self._native.uint32_field = _unwrap(value, Optional[int])


    @property
    def uint64_field(self):
        return _wrap(self._native.uint64_field, Optional[int])
    @uint64_field.setter
    def uint64_field(self, value):
      self._native.uint64_field = _unwrap(value, Optional[int])


