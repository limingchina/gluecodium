

from dontsmoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable

from _native_base import _NativeBase


class SerializableStructWithExternalField(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    some_struct: ExternalMarkedAsSerializable

