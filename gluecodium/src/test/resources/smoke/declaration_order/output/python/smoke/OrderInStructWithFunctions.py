

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class OrderInStructWithFunctions(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OrderInStructWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OrderInStructWithFunctions(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def some_field(self) -> str:
        return _wrap(self._native.some_field, str)
    @some_field.setter
    def some_field(self, value: str):
      self._native.some_field = _unwrap(value, str)


    def do_stuff(self, struct_foo: OrderInStructWithFunctions.NestedStruct) -> OrderInStructWithFunctions.SomeEnum:
        return _wrap(self._native.do_stuff(_unwrap(struct_foo, OrderInStructWithFunctions.NestedStruct)), OrderInStructWithFunctions.SomeEnum)

    class NestedStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OrderInStructWithFunctions.NestedStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_OrderInStructWithFunctions.NestedStruct(
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
    
        FOO = generated.smoke_OrderInStructWithFunctions.SomeEnum.FOO
        BAR = generated.smoke_OrderInStructWithFunctions.SomeEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    

