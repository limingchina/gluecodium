

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class OrderInClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class MainStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OrderInClassMainStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_OrderInClassMainStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> OrderInClass.NestedStruct:
            return _wrap(self._native.struct_field, OrderInClass.NestedStruct)
        @struct_field.setter
        def struct_field(self, value: OrderInClass.NestedStruct):
          self._native.struct_field = _unwrap(value, OrderInClass.NestedStruct)
    
    
        @property
        def type_def_field(self) -> int:
            return _wrap(self._native.type_def_field, int)
        @type_def_field.setter
        def type_def_field(self, value: int):
          self._native.type_def_field = _unwrap(value, int)
    
    
        @property
        def struct_array_field(self) -> list[OrderInClass.NestedStruct]:
            return _wrap(self._native.struct_array_field, list[OrderInClass.NestedStruct])
        @struct_array_field.setter
        def struct_array_field(self, value: list[OrderInClass.NestedStruct]):
          self._native.struct_array_field = _unwrap(value, list[OrderInClass.NestedStruct])
    
    
        @property
        def map_field(self) -> dict[int, list[OrderInClass.NestedStruct]]:
            return _wrap(self._native.map_field, dict[int, list[OrderInClass.NestedStruct]])
        @map_field.setter
        def map_field(self, value: dict[int, list[OrderInClass.NestedStruct]]):
          self._native.map_field = _unwrap(value, dict[int, list[OrderInClass.NestedStruct]])
    
    
        @property
        def enum_field(self) -> OrderInClass.SomeEnum:
            return _wrap(self._native.enum_field, OrderInClass.SomeEnum)
        @enum_field.setter
        def enum_field(self, value: OrderInClass.SomeEnum):
          self._native.enum_field = _unwrap(value, OrderInClass.SomeEnum)
    
    
    
    
    class NestedStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OrderInClassNestedStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_OrderInClassNestedStruct(
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
    
        FOO = 0
        BAR = 1
    
    
    
    int = int
    
    
    
    dict[int, list[OrderInClass.NestedStruct]] = dict[int, list[OrderInClass.NestedStruct]]
    
    
    
    list[OrderInClass.NestedStruct] = list[OrderInClass.NestedStruct]
    
    

