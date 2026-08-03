

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class DeclarationOrder(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrder):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeclarationOrder(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class MainStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrder.MainStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrder.MainStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> DeclarationOrder.NestedStruct:
            return _wrap(self._native.struct_field, DeclarationOrder.NestedStruct)
        @struct_field.setter
        def struct_field(self, value: DeclarationOrder.NestedStruct):
          self._native.struct_field = _unwrap(value, DeclarationOrder.NestedStruct)
    
    
        @property
        def type_def_field(self) -> int:
            return _wrap(self._native.type_def_field, int)
        @type_def_field.setter
        def type_def_field(self, value: int):
          self._native.type_def_field = _unwrap(value, int)
    
    
        @property
        def struct_array_field(self) -> list[DeclarationOrder.NestedStruct]:
            return _wrap(self._native.struct_array_field, list[DeclarationOrder.NestedStruct])
        @struct_array_field.setter
        def struct_array_field(self, value: list[DeclarationOrder.NestedStruct]):
          self._native.struct_array_field = _unwrap(value, list[DeclarationOrder.NestedStruct])
    
    
        @property
        def map_field(self) -> dict[int, list[DeclarationOrder.NestedStruct]]:
            return _wrap(self._native.map_field, dict[int, list[DeclarationOrder.NestedStruct]])
        @map_field.setter
        def map_field(self, value: dict[int, list[DeclarationOrder.NestedStruct]]):
          self._native.map_field = _unwrap(value, dict[int, list[DeclarationOrder.NestedStruct]])
    
    
        @property
        def enum_field(self) -> DeclarationOrder.SomeEnum:
            return _wrap(self._native.enum_field, DeclarationOrder.SomeEnum)
        @enum_field.setter
        def enum_field(self, value: DeclarationOrder.SomeEnum):
          self._native.enum_field = _unwrap(value, DeclarationOrder.SomeEnum)
    
    
    
    
    class NestedStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrder.NestedStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeclarationOrder.NestedStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class SomeEnum(Enum):
    
        FOO = generated.smoke_DeclarationOrder.SomeEnum.FOO
        BAR = generated.smoke_DeclarationOrder.SomeEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    
    
    SomeTypeDef = int
    
    
    
    ErrorCodeToMessageMap = dict[int, list[NestedStruct]]
    
    
    
    NestedStructArray = list[NestedStruct]
    
    

