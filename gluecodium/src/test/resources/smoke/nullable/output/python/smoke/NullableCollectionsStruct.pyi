

import datetime
from smoke.Nullable import Nullable
from enum import Enum
import typing

class NullableCollectionsStruct:

    dates: list[Optional[datetime.datetime]]

    structs: dict[int, Optional[Nullable.SomeStruct]]


