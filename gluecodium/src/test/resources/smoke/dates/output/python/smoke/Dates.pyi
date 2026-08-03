

import datetime
from enum import Enum
import typing

class Dates:

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        ...

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        ...

    @property
    def date_property(self) -> datetime.datetime:
        ...

    @date_property.setter
    def date_property(self, value: datetime.datetime) -> None:
        ...

    @property
    def date_set(self) -> set[datetime.datetime]:
        ...

    @date_set.setter
    def date_set(self, value: set[datetime.datetime]) -> None:
        ...

    class DateStruct:
    
        date_field: datetime.datetime
    
        nullable_date_field: Optional[datetime.datetime]
    
    
    
    DateTypeDef = datetime.datetime
    
    
    
    DateArray = list[datetime.datetime]
    
    
    
    DateMap = dict[str, datetime.datetime]
    
    

