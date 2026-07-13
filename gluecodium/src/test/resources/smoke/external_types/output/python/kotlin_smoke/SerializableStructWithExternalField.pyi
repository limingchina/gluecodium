

from kotlin_smoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable


from _native_base import _NativeBase

import generated


class SerializableStructWithExternalField(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SerializableStructWithExternalField):
            super().__init__(args[0])
        else:
            super().__init__(generated.SerializableStructWithExternalField(*args))


    @property
    def some_struct(self) -> ExternalMarkedAsSerializable:
        """"""
        return self._native.some_struct

    @some_struct.setter
    def some_struct(self, value: ExternalMarkedAsSerializable):
        self._native.some_struct = value


