

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
    
    
    
    datetime.datetime = datetime.datetime
    
    
    
    list[datetime.datetime] = list[datetime.datetime]
    
    
    
    dict[datetime.datetime, str] = dict[datetime.datetime, str]
    
    

