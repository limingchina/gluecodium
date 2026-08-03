

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class RouteUtils(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_RouteUtils):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_RouteUtils(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class RouteType(Enum):
    
        NONE = generated.smoke_RouteUtils.RouteType.NONE
        CAR = generated.smoke_RouteUtils.RouteType.CAR
        PEDESTRIAN = generated.smoke_RouteUtils.RouteType.PEDESTRIAN
        EQUESTRIAN = generated.smoke_RouteUtils.RouteType.EQUESTRIAN
    
        @property
        def _native(self):
            return self.value
    
    

