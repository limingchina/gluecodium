

from kotlin_smoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable
import typing


from _native_base import _NativeBase

import generated


class SerializableStructWithExternalField(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.kotlin_smoke_SerializableStructWithExternalField):
            super().__init__(args[0])
        else:
            super().__init__(generated.kotlin_smoke_SerializableStructWithExternalField(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def some_struct(self) -> ExternalMarkedAsSerializable:
        """"""
        return _wrap(self._native.some_struct, ExternalMarkedAsSerializable)
    @some_struct.setter
    def some_struct(self, value: ExternalMarkedAsSerializable):
      self._native.some_struct = _unwrap(value, ExternalMarkedAsSerializable)


