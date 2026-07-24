

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from fire.SomeStruct import SomeStruct


from _native_base import _NativeBase

import generated


class ConstantDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ConstantDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.ConstantDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def field1(self) -> SomeStruct:
        """"""
        return _wrap(self._native.field1, SomeStruct)
    @field1.setter
    def field1(self, value: SomeStruct):
      self._native.field1 = _unwrap(value, SomeStruct)



    @property
    def field2(self) -> SomeStruct:
        """"""
        return _wrap(self._native.field2, SomeStruct)
    @field2.setter
    def field2(self, value: SomeStruct):
      self._native.field2 = _unwrap(value, SomeStruct)


