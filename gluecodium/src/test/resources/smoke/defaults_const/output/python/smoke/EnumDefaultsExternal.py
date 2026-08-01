

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from fire.ExternalEnum1 import ExternalEnum1
from fire.ExternalEnum2 import ExternalEnum2
from fire.ExternalEnum3 import ExternalEnum3
from fire.ExternalEnum4 import ExternalEnum4
from smoke.EnumWrapper import EnumWrapper

class EnumDefaultsExternal(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class SimpleEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsExternalSimpleEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsExternalSimpleEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def enum_field(self) -> ExternalEnum1:
            return _wrap(self._native.enum_field, ExternalEnum1)
        @enum_field.setter
        def enum_field(self, value: ExternalEnum1):
          self._native.enum_field = _unwrap(value, ExternalEnum1)
    
    
    
    
    class NullableEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsExternalNullableEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsExternalNullableEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def enum_field1(self):
            return _wrap(self._native.enum_field1, Optional[ExternalEnum2])
        @enum_field1.setter
        def enum_field1(self, value):
          self._native.enum_field1 = _unwrap(value, Optional[ExternalEnum2])
    
    
        @property
        def enum_field2(self):
            return _wrap(self._native.enum_field2, Optional[ExternalEnum2])
        @enum_field2.setter
        def enum_field2(self, value):
          self._native.enum_field2 = _unwrap(value, Optional[ExternalEnum2])
    
    
    
    
    class AliasEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsExternalAliasEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsExternalAliasEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def enum_field(self) -> ExternalEnum3:
            return _wrap(self._native.enum_field, ExternalEnum3)
        @enum_field.setter
        def enum_field(self, value: ExternalEnum3):
          self._native.enum_field = _unwrap(value, ExternalEnum3)
    
    
    
    
    class WrappedEnum(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsExternalWrappedEnum):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumDefaultsExternalWrappedEnum(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> EnumWrapper:
            return _wrap(self._native.struct_field, EnumWrapper)
        @struct_field.setter
        def struct_field(self, value: EnumWrapper):
          self._native.struct_field = _unwrap(value, EnumWrapper)
    
    
    
    
    ExternalEnum3 = ExternalEnum3
    
    

