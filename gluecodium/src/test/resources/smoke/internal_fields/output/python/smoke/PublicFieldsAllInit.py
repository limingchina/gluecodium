

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class PublicFieldsAllInit(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PublicFieldsAllInit):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicFieldsAllInit(*[_unwrap(arg) for arg in args]))


    @property
    def public_field(self) -> str:
        """"""
        return _wrap(self._native.public_field, str)
    @public_field.setter
    def public_field(self, value: str):
      self._native.public_field = _unwrap(value, str)



    @property
    def internal_field(self) -> str:
        """"""
        return _wrap(self._native.internal_field, str)
    @internal_field.setter
    def internal_field(self, value: str):
      self._native.internal_field = _unwrap(value, str)


