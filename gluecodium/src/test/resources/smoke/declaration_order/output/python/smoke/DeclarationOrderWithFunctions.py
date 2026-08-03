

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class DeclarationOrderWithFunctions(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeclarationOrderWithFunctions(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class MainStructWithFunctions(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctions.MainStructWithFunctions):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrderWithFunctions.MainStructWithFunctions(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> DeclarationOrderWithFunctions.FieldStruct:
            return _wrap(self._native.struct_field, DeclarationOrderWithFunctions.FieldStruct)
        @struct_field.setter
        def struct_field(self, value: DeclarationOrderWithFunctions.FieldStruct):
          self._native.struct_field = _unwrap(value, DeclarationOrderWithFunctions.FieldStruct)
    
    
        def with_parameter(self, input: DeclarationOrderWithFunctions.ParameterStruct):
            return _wrap(self._native.with_parameter(_unwrap(input, DeclarationOrderWithFunctions.ParameterStruct)), None)
    
        def with_return(self) -> DeclarationOrderWithFunctions.ReturnStruct:
            return _wrap(self._native.with_return(), DeclarationOrderWithFunctions.ReturnStruct)
    
        def with_thrown(self):
            return _wrap(self._native.with_thrown(), None)
    
    
    
    class FieldStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctions.FieldStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrderWithFunctions.FieldStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class ParameterStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctions.ParameterStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrderWithFunctions.ParameterStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class ReturnStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctions.ReturnStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrderWithFunctions.ReturnStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class ThrownStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctions.ThrownStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrderWithFunctions.ThrownStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class FooBarError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

