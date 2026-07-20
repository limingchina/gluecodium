

from kotlin_smoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable
import typing


from _native_base import _NativeBase

import generated


class SerializableStructWithExternalField(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SerializableStructWithExternalField):
            super().__init__(args[0])
        else:
            super().__init__(generated.SerializableStructWithExternalField(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_struct(self) -> ExternalMarkedAsSerializable:
        """"""
        return ExternalMarkedAsSerializable(self._native.some_struct)
    @some_struct.setter
    def some_struct(self, value: ExternalMarkedAsSerializable):
      self._native.some_struct = getattr(value, "_native", value)


