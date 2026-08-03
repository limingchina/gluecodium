

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class AttributesWithDeprecated(_NativeBase):
    """"""
    def __init__(self, native):
        super().__init__(native)

    def very_fun(self):
        """"""
        return _wrap(self._native.very_fun(), None)

    @property
    def prop(self) -> str:
        """"""
        return _wrap(self._native.prop, str)

    @prop.setter
    def prop(self, value: str):
        self._native.prop = _unwrap(value, str)

    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_AttributesWithDeprecatedSomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_AttributesWithDeprecatedSomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def field(self) -> str:
            """"""
            return _wrap(self._native.field, str)
        @field.setter
        def field(self, value: str):
          self._native.field = _unwrap(value, str)
    
    
    

    #: 
    PI = False

