

from dontsmoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable

class SerializableStructWithExternalField:
    """"""

    def __init__(self, native):
        self._native = native


    some_struct: ExternalMarkedAsSerializable

