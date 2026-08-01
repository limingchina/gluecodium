

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Locales(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def locale_method(self, input: str) -> str:
        return _wrap(self._native.locale_method(_unwrap(input, str)), str)

    @property
    def locale_property(self) -> str:
        return _wrap(self._native.locale_property, str)

    @locale_property.setter
    def locale_property(self, value: str):
        self._native.locale_property = _unwrap(value, str)

    class LocaleStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_LocalesLocaleStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_LocalesLocaleStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def locale_field(self) -> str:
            return _wrap(self._native.locale_field, str)
        @locale_field.setter
        def locale_field(self, value: str):
          self._native.locale_field = _unwrap(value, str)
    
    
    
    
    str = str
    
    
    
    list[str] = list[str]
    
    
    
    dict[str, str] = dict[str, str]
    
    
    
    set[str] = set[str]
    
    
    
    dict[str, str] = dict[str, str]
    
    

