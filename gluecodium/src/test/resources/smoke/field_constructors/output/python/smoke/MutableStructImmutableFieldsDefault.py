

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ImmutableDefaultCtor import ImmutableDefaultCtor


from _native_base import _NativeBase

import generated


class MutableStructImmutableFieldsDefault(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_MutableStructImmutableFieldsDefault):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_MutableStructImmutableFieldsDefault(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def struct_field(self) -> ImmutableDefaultCtor:
        return _wrap(self._native.struct_field, ImmutableDefaultCtor)
    @struct_field.setter
    def struct_field(self, value: ImmutableDefaultCtor):
      self._native.struct_field = _unwrap(value, ImmutableDefaultCtor)


    @property
    def int_field(self) -> int:
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)


    @property
    def bool_field(self) -> bool:
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)


