

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class ExternalMarkedAsSerializable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.dontsmoke_ExternalMarkedAsSerializable):
            super().__init__(args[0])
        else:
            super().__init__(generated.dontsmoke_ExternalMarkedAsSerializable(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> int:
        """"""
        return _wrap(self._native.field, int)
    @field.setter
    def field(self, value: int):
      self._native.field = _unwrap(value, int)


