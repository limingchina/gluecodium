

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class PublicClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def _internal_method(self, input: PublicClass._InternalStruct) -> PublicClass._InternalStruct:
        return _wrap(self._native._internal_method(_unwrap(input, PublicClass._InternalStruct)), PublicClass._InternalStruct)

    @property
    def __internal_struct_property(self) -> PublicClass._InternalStruct:
        return _wrap(self._native.__internal_struct_property, PublicClass._InternalStruct)

    @__internal_struct_property.setter
    def __internal_struct_property(self, value: PublicClass._InternalStruct):
        self._native.__internal_struct_property = _unwrap(value, PublicClass._InternalStruct)

    class _InternalStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicClass._InternalStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PublicClass._InternalStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
    
    
    class PublicStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicClass.PublicStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PublicClass.PublicStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def _internal_field(self) -> PublicClass._InternalStruct:
            return _wrap(self._native._internal_field, PublicClass._InternalStruct)
        @_internal_field.setter
        def _internal_field(self, value: PublicClass._InternalStruct):
          self._native._internal_field = _unwrap(value, PublicClass._InternalStruct)
    
    
    
    
    class PublicStructWithInternalDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicClass.PublicStructWithInternalDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PublicClass.PublicStructWithInternalDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def _internal_field(self) -> str:
            return _wrap(self._native._internal_field, str)
        @_internal_field.setter
        def _internal_field(self, value: str):
          self._native._internal_field = _unwrap(value, str)
    
    
        @property
        def public_field(self) -> float:
            return _wrap(self._native.public_field, float)
        @public_field.setter
        def public_field(self, value: float):
          self._native.public_field = _unwrap(value, float)
    
    
    
    
    class _InternalEnum(Enum):
    
        FOO = generated.smoke_PublicClass._InternalEnum.FOO
        BAR = generated.smoke_PublicClass._InternalEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    
    
    _InternalArray = list[_InternalStruct]
    
    
    
    _InternalStructTypeDef = _InternalStruct
    
    
    
    _StringToInternalStructMap = dict[str, _InternalStruct]
    
    

