

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class PublicClassPublicStructWithInternalDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PublicClassPublicStructWithInternalDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.PublicClassPublicStructWithInternalDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def internal_field(self) -> str:
        """"""
        return _wrap(self._native.internal_field, str)
    @internal_field.setter
    def internal_field(self, value: str):
      self._native.internal_field = _unwrap(value, str)



    @property
    def public_field(self) -> float:
        """"""
        return _wrap(self._native.public_field, float)
    @public_field.setter
    def public_field(self, value: float):
      self._native.public_field = _unwrap(value, float)


