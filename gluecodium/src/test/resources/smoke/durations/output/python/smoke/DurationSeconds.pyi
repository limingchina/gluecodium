

import datetime
import typing

class DurationSeconds:

    def duration_function(self, input: datetime.timedelta) -> datetime.timedelta:
        ...

    def nullable_duration_function(self, input: Optional[datetime.timedelta]) -> Optional[datetime.timedelta]:
        ...

    @property
    def duration_property(self) -> datetime.timedelta:
        ...

    @duration_property.setter
    def duration_property(self, value: datetime.timedelta) -> None:
        ...

