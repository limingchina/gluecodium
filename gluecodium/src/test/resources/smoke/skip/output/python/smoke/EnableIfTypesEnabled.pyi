

from enum import Enum
import typing
from typing import Optional

class EnableIfTypesEnabled:
    def __init__(self) -> None: ...

    class EnableMeToo:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, field: EnableIfTypesEnabled.EnableMe) -> None: ...

        field: EnableIfTypesEnabled.EnableMe



    class EnableMe(Enum):

        NOPE = 0



    PLACE_HOLDER_ENABLED = True
