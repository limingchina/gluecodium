

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.RouteUtils import RouteUtils

class StructsWithConstantsInterface(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class MultiRoute(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithConstantsInterfaceMultiRoute):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsWithConstantsInterfaceMultiRoute(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def descriptions(self) -> list[str]:
            return _wrap(self._native.descriptions, list[str])
        @descriptions.setter
        def descriptions(self, value: list[str]):
          self._native.descriptions = _unwrap(value, list[str])
    
    
        @property
        def type(self) -> RouteUtils.RouteType:
            return _wrap(self._native.type, RouteUtils.RouteType)
        @type.setter
        def type(self, value: RouteUtils.RouteType):
          self._native.type = _unwrap(value, RouteUtils.RouteType)
    
    
        DEFAULT_DESCRIPTION = "Foo"
    
        DEFAULT_TYPE = RouteType.NONE
    
    
    
    class StructWithConstantsOnly(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithConstantsInterfaceStructWithConstantsOnly):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsWithConstantsInterfaceStructWithConstantsOnly(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        DEFAULT_DESCRIPTION = "Foo"
    
    

