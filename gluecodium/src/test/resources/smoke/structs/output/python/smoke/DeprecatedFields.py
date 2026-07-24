

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class DeprecatedFields(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DeprecatedFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeprecatedFields(*[_unwrap(arg) for arg in args]))


    @property
    def normal_field1(self) -> str:
        """"""
        return _wrap(self._native.normal_field1, str)
    @normal_field1.setter
    def normal_field1(self, value: str):
      self._native.normal_field1 = _unwrap(value, str)



    @property
    def deprecated_field(self) -> str:
        """"""
        return _wrap(self._native.deprecated_field, str)
    @deprecated_field.setter
    def deprecated_field(self, value: str):
      self._native.deprecated_field = _unwrap(value, str)



    @property
    def normal_field2(self) -> str:
        """"""
        return _wrap(self._native.normal_field2, str)
    @normal_field2.setter
    def normal_field2(self, value: str):
      self._native.normal_field2 = _unwrap(value, str)


