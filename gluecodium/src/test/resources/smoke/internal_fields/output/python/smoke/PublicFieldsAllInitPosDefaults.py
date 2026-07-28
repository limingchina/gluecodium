

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class PublicFieldsAllInitPosDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicFieldsAllInitPosDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicFieldsAllInitPosDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


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


