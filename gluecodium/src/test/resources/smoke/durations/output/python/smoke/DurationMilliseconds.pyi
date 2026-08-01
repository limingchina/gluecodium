

import datetime
from enum import Enum
import typing

class DurationMilliseconds:

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

    class DurationStruct:
    
        duration_field: datetime.timedelta
    
    
    
    datetime.timedelta = datetime.timedelta
    
    
    
    list[datetime.timedelta] = list[datetime.timedelta]
    
    
    
    set[datetime.timedelta] = set[datetime.timedelta]
    
    
    
    dict[str, datetime.timedelta] = dict[str, datetime.timedelta]
    
    
    
    dict[datetime.timedelta, str] = dict[datetime.timedelta, str]
    
    

