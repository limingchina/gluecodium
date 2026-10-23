

from enum import Enum
import typing
from typing import Optional

class BlobDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, empty_list: bytes, dead_beef: bytes) -> None: ...

    empty_list: bytes

    dead_beef: bytes
