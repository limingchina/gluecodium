

import datetime
from smoke.Nullable import Nullable
from enum import Enum
import typing
from typing import Optional

class NullableCollectionsStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dates: list[Optional[datetime.datetime]], structs: dict[int, Optional[Nullable.SomeStruct]]) -> None: ...

    dates: list[Optional[datetime.datetime]]

    structs: dict[int, Optional[Nullable.SomeStruct]]
