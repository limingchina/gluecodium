

import datetime
from enum import Enum
import typing

class DatesSteady:

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        ...

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        ...

    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        ...

    class DateStruct:
    
        date_field: datetime.datetime
    
        nullable_date_field: Optional[datetime.datetime]
    
    
    
    MonotonicDate = datetime.datetime
    
    
    
    DateList = list[datetime.datetime]
    
    
    
    DateMap = dict[datetime.datetime, str]
    
    

