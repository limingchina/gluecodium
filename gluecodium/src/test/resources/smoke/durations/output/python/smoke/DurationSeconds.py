

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

import datetime

class DurationSeconds(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def duration_function(self, input: datetime.timedelta) -> datetime.timedelta:
        return _wrap(self._native.duration_function(_unwrap(input, datetime.timedelta)), datetime.timedelta)

    def nullable_duration_function(self, input: Optional[datetime.timedelta]) -> Optional[datetime.timedelta]:
        return _wrap(self._native.nullable_duration_function(_unwrap(input, Optional[datetime.timedelta])), Optional[datetime.timedelta])

    @property
    def duration_property(self) -> datetime.timedelta:
        return _wrap(self._native.duration_property, datetime.timedelta)

    @duration_property.setter
    def duration_property(self, value: datetime.timedelta):
        self._native.duration_property = _unwrap(value, datetime.timedelta)

    class DurationStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DurationSecondsDurationStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DurationSecondsDurationStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def duration_field(self) -> datetime.timedelta:
            return _wrap(self._native.duration_field, datetime.timedelta)
        @duration_field.setter
        def duration_field(self, value: datetime.timedelta):
          self._native.duration_field = _unwrap(value, datetime.timedelta)
    
    
    
    
    DurationTypeAlias = datetime.timedelta
    
    
    
    DurationList = list[datetime.timedelta]
    
    
    
    DurationSet = set[datetime.timedelta]
    
    
    
    DurationMap = dict[str, datetime.timedelta]
    
    
    
    DurationKeyMap = dict[datetime.timedelta, str]
    
    

