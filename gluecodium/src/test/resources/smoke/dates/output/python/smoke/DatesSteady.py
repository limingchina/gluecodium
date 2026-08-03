

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

import datetime

class DatesSteady(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        return _wrap(self._native.date_method(_unwrap(input, datetime.datetime)), datetime.datetime)

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        return _wrap(self._native.nullable_date_method(_unwrap(input, Optional[datetime.datetime])), Optional[datetime.datetime])

    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        return _wrap(self._native.date_list_method(_unwrap(input, list[datetime.datetime])), list[datetime.datetime])

    class DateStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DatesSteadyDateStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DatesSteadyDateStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def date_field(self) -> datetime.datetime:
            return _wrap(self._native.date_field, datetime.datetime)
        @date_field.setter
        def date_field(self, value: datetime.datetime):
          self._native.date_field = _unwrap(value, datetime.datetime)
    
    
        @property
        def nullable_date_field(self):
            return _wrap(self._native.nullable_date_field, Optional[datetime.datetime])
        @nullable_date_field.setter
        def nullable_date_field(self, value):
          self._native.nullable_date_field = _unwrap(value, Optional[datetime.datetime])
    
    
    
    
    MonotonicDate = datetime.datetime
    
    
    
    DateList = list[datetime.datetime]
    
    
    
    DateMap = dict[datetime.datetime, str]
    
    

