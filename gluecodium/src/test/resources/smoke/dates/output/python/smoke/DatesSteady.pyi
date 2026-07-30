

import datetime
import typing

class DatesSteady:

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        ...

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        ...

    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        ...

