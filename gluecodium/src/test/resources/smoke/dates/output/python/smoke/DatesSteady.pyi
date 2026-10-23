

import datetime
from enum import Enum
import typing
from typing import Optional

class DatesSteady:

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        ...

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        ...

    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        ...

    class DateStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, date_field: datetime.datetime) -> None: ...
        @typing.overload
        def __init__(self, date_field: datetime.datetime, nullable_date_field: Optional[datetime.datetime]) -> None: ...

        date_field: datetime.datetime

        nullable_date_field: Optional[datetime.datetime]



    MonotonicDate = datetime.datetime



    DateList = list[datetime.datetime]



    DateMap = dict[datetime.datetime, str]
