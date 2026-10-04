

from smoke.PublicClass import PublicClass
from enum import Enum
import typing
from typing import Optional

class PublicInterface:

    class _InternalStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, field_of_internal_type: PublicClass._InternalStruct) -> None: ...

        field_of_internal_type: PublicClass._InternalStruct
