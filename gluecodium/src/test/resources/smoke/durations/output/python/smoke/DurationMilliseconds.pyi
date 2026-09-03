

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
    
    
    
    DurationTypeAlias = datetime.timedelta
    
    
    
    DurationList = list[datetime.timedelta]
    
    
    
    DurationSet = set[datetime.timedelta]
    
    
    
    DurationMap = dict[str, datetime.timedelta]
    
    
    
    DurationKeyMap = dict[datetime.timedelta, str]
    
    

