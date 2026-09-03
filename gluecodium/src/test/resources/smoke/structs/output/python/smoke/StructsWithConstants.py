

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.RouteUtils import RouteUtils

class StructsWithConstants(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithConstants(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class Route(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithConstants.Route):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsWithConstants.Route(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def description(self) -> str:
            return _wrap(self._native.description, str)
        @description.setter
        def description(self, value: str):
          self._native.description = _unwrap(value, str)
    
    
        @property
        def type(self) -> RouteUtils.RouteType:
            return _wrap(self._native.type, RouteUtils.RouteType)
        @type.setter
        def type(self, value: RouteUtils.RouteType):
          self._native.type = _unwrap(value, RouteUtils.RouteType)
    
    
    
        DEFAULT_DESCRIPTION = "Nonsense"
    
        DEFAULT_TYPE = RouteUtils.RouteType.EQUESTRIAN
    

