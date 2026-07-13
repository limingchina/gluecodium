

import datetime
from smoke.datetime.datetime import datetime.datetime
from smoke.list[datetime.datetime] import list[datetime.datetime]

class DatesSteady:
    """"""

    def __init__(self, native):
        self._native = native


    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        """"""
        return self._native.date_method(input)


    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """"""
        return self._native.nullable_date_method(input)


    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        """"""
        return self._native.date_list_method(input)

