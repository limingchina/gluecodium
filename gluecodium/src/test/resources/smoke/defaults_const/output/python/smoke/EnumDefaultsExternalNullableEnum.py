

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from fire.ExternalEnum2 import ExternalEnum2


from _native_base import _NativeBase

import generated


class EnumDefaultsExternalNullableEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsExternalNullableEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsExternalNullableEnum(*[_unwrap(arg) for arg in args]))


    @property
    def enum_field1(self):
        """"""
        return _wrap(self._native.enum_field1, Optional[ExternalEnum2])
    @enum_field1.setter
    def enum_field1(self, value):
      self._native.enum_field1 = _unwrap(value, Optional[ExternalEnum2])



    @property
    def enum_field2(self):
        """"""
        return _wrap(self._native.enum_field2, Optional[ExternalEnum2])
    @enum_field2.setter
    def enum_field2(self, value):
      self._native.enum_field2 = _unwrap(value, Optional[ExternalEnum2])


