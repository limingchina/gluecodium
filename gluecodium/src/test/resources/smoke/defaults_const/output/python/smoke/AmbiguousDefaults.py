

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.AmbiguousEnum import AmbiguousEnum
from fire.SomeStruct import SomeStruct


from _native_base import _NativeBase

import generated


class AmbiguousDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_AmbiguousDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_AmbiguousDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def field1(self) -> AmbiguousEnum:
        """"""
        return _wrap(self._native.field1, AmbiguousEnum)
    @field1.setter
    def field1(self, value: AmbiguousEnum):
      self._native.field1 = _unwrap(value, AmbiguousEnum)



    @property
    def field2(self) -> SomeStruct:
        """"""
        return _wrap(self._native.field2, SomeStruct)
    @field2.setter
    def field2(self, value: SomeStruct):
      self._native.field2 = _unwrap(value, SomeStruct)


