

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4
from smoke.EnumWrapper import EnumWrapper

class EnumDefaults(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class SimpleEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsSimpleEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsSimpleEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def enum_field(self) -> Enum1:
            return _wrap(self._native.enum_field, Enum1)
        @enum_field.setter
        def enum_field(self, value: Enum1):
          self._native.enum_field = _unwrap(value, Enum1)
    
    
    
    
    class NullableEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsNullableEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsNullableEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def enum_field1(self):
            return _wrap(self._native.enum_field1, Optional[Enum2])
        @enum_field1.setter
        def enum_field1(self, value):
          self._native.enum_field1 = _unwrap(value, Optional[Enum2])
    
    
        @property
        def enum_field1(self):
            return _wrap(self._native.enum_field1, Optional[Enum2])
        @enum_field1.setter
        def enum_field1(self, value):
          self._native.enum_field1 = _unwrap(value, Optional[Enum2])
    
    
    
    
    class AliasEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsAliasEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsAliasEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def enum_field(self) -> Enum3:
            return _wrap(self._native.enum_field, Enum3)
        @enum_field.setter
        def enum_field(self, value: Enum3):
          self._native.enum_field = _unwrap(value, Enum3)
    
    
    
    
    class WrappedEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsWrappedEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsWrappedEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> EnumWrapper:
            return _wrap(self._native.struct_field, EnumWrapper)
        @struct_field.setter
        def struct_field(self, value: EnumWrapper):
          self._native.struct_field = _unwrap(value, EnumWrapper)
    
    
    
    
    Enum3 = Enum3
    
    

