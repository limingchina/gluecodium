

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class PublicStructWithNonDefaultInternalField(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PublicStructWithNonDefaultInternalField):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicStructWithNonDefaultInternalField(*[_unwrap(arg) for arg in args]))


    @property
    def defaulted_field(self) -> int:
        """"""
        return _wrap(self._native.defaulted_field, int)
    @defaulted_field.setter
    def defaulted_field(self, value: int):
      self._native.defaulted_field = _unwrap(value, int)



    @property
    def internal_field(self) -> str:
        """"""
        return _wrap(self._native.internal_field, str)
    @internal_field.setter
    def internal_field(self, value: str):
      self._native.internal_field = _unwrap(value, str)



    @property
    def public_field(self) -> bool:
        """"""
        return _wrap(self._native.public_field, bool)
    @public_field.setter
    def public_field(self, value: bool):
      self._native.public_field = _unwrap(value, bool)


