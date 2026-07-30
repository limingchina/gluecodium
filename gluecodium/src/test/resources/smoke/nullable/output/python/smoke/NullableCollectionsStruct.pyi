

import datetime
from smoke.NullableSomeStruct import NullableSomeStruct
import typing

class NullableCollectionsStruct:

    dates: list[Optional[datetime.datetime]]

    structs: dict[int, Optional[NullableSomeStruct]]

