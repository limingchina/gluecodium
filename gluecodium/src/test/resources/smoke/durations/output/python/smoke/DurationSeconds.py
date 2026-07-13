

import datetime

class DurationSeconds:
    """"""

    def __init__(self, native):
        self._native = native


    def duration_function(self, input: datetime.timedelta) -> datetime.timedelta:
        """"""
        return self._native.duration_function(input)


    def nullable_duration_function(self, input: Optional[datetime.timedelta]) -> Optional[datetime.timedelta]:
        """"""
        return self._native.nullable_duration_function(input)


    @property
    def duration_property(self) -> datetime.timedelta:
        """"""
        return self._native.duration_property


