

import datetime

class Dates:
    """"""

    def __init__(self, native):
        self._native = native


    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        """"""
        return self._native.date_method(input)


    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """"""
        return self._native.nullable_date_method(input)


    @property
    def date_property(self) -> datetime.datetime:
        """"""
        return self._native.date_property



    @property
    def date_set(self) -> set[datetime.datetime]:
        """"""
        return self._native.date_set


