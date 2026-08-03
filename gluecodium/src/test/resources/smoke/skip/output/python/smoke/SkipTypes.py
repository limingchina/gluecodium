

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SkipTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class NotInJava(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SkipTypes.NotInJava):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_SkipTypes.NotInJava(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def foo_field(self) -> str:
            return _wrap(self._native.foo_field, str)
        @foo_field.setter
        def foo_field(self, value: str):
          self._native.foo_field = _unwrap(value, str)
    
    
    
    
    class NotInSwift(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SkipTypes.NotInSwift):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_SkipTypes.NotInSwift(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def foo_field(self) -> str:
            return _wrap(self._native.foo_field, str)
        @foo_field.setter
        def foo_field(self, value: str):
          self._native.foo_field = _unwrap(value, str)
    
    
    
    
    class NotInDart(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SkipTypes.NotInDart):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_SkipTypes.NotInDart(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def foo_field(self) -> str:
            return _wrap(self._native.foo_field, str)
        @foo_field.setter
        def foo_field(self, value: str):
          self._native.foo_field = _unwrap(value, str)
    
    
    
    
    class NotInKotlin(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SkipTypes.NotInKotlin):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_SkipTypes.NotInKotlin(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def foo_field(self) -> str:
            return _wrap(self._native.foo_field, str)
        @foo_field.setter
        def foo_field(self, value: str):
          self._native.foo_field = _unwrap(value, str)
    
    
    

