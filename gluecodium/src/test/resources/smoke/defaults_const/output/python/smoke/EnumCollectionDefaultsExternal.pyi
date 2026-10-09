

from fire.ExternalEnum1 import ExternalEnum1
from fire.ExternalEnum2 import ExternalEnum2
from fire.ExternalEnum3 import ExternalEnum3
from fire.ExternalEnum4 import ExternalEnum4
from enum import Enum
import typing
from typing import Optional

class EnumCollectionDefaultsExternal:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, list_field: list[ExternalEnum1], set_field: set[ExternalEnum2], map_field: dict[ExternalEnum3, ExternalEnum4]) -> None: ...

    list_field: list[ExternalEnum1]

    set_field: set[ExternalEnum2]

    map_field: dict[ExternalEnum3, ExternalEnum4]
