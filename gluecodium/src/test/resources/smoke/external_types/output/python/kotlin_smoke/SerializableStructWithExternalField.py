

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from kotlin_smoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable


from _native_base import _NativeBase

import generated


class SerializableStructWithExternalField(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SerializableStructWithExternalField):
            super().__init__(args[0])
        else:
            super().__init__(generated.SerializableStructWithExternalField(*[_unwrap(arg) for arg in args]))


    @property
    def some_struct(self) -> ExternalMarkedAsSerializable:
        """"""
        return _wrap(self._native.some_struct, ExternalMarkedAsSerializable)
    @some_struct.setter
    def some_struct(self, value: ExternalMarkedAsSerializable):
      self._native.some_struct = _unwrap(value, ExternalMarkedAsSerializable)


