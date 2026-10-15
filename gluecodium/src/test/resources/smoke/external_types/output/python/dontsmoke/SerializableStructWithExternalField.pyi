

from dontsmoke.ExternalMarkedAsSerializable import ExternalMarkedAsSerializable
from enum import Enum
import typing
from typing import Optional

class SerializableStructWithExternalField:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, some_struct: ExternalMarkedAsSerializable) -> None: ...

    some_struct: ExternalMarkedAsSerializable
