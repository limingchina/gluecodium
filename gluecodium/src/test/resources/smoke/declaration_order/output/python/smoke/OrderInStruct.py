

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class OrderInStruct(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OrderInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OrderInStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def struct_field(self) -> OrderInStruct.NestedStruct:
        return _wrap(self._native.struct_field, OrderInStruct.NestedStruct)
    @struct_field.setter
    def struct_field(self, value: OrderInStruct.NestedStruct):
      self._native.struct_field = _unwrap(value, OrderInStruct.NestedStruct)


    @property
    def enum_field(self) -> OrderInStruct.SomeEnum:
        return _wrap(self._native.enum_field, OrderInStruct.SomeEnum)
    @enum_field.setter
    def enum_field(self, value: OrderInStruct.SomeEnum):
      self._native.enum_field = _unwrap(value, OrderInStruct.SomeEnum)


    class NestedStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OrderInStruct.NestedStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_OrderInStruct.NestedStruct(
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
    
        FOO = generated.smoke_OrderInStruct.SomeEnum.FOO
        BAR = generated.smoke_OrderInStruct.SomeEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    

