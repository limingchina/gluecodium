

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated

import datetime

class OuterStruct(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def field(self) -> str:
        return _wrap(self._native.field, str)
    @field.setter
    def field(self, value: str):
      self._native.field = _unwrap(value, str)


    def do_nothing(self):
        return _wrap(self._native.do_nothing(), None)

    class InnerStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStructInnerStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_OuterStructInnerStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def other_field(self) -> list[datetime.datetime]:
            return _wrap(self._native.other_field, list[datetime.datetime])
        @other_field.setter
        def other_field(self, value: list[datetime.datetime]):
          self._native.other_field = _unwrap(value, list[datetime.datetime])
    
    
        def do_something(self):
            return _wrap(self._native.do_something(), None)
    
    
    
    class InnerClass(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        def foo_bar(self) -> set[str]:
            return _wrap(self._native.foo_bar(), set[str])
    
    
    
    class Builder(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create() -> OuterStruct.Builder:
            native_result = generated.smoke_OuterStructBuilder.create()
            return _get_or_create_wrapper(native_result, OuterStruct.Builder)
    
        def field(self, value: str) -> OuterStruct.Builder:
            return _wrap(self._native.field(_unwrap(value, str)), OuterStruct.Builder)
    
        def build(self) -> OuterStruct:
            return _wrap(self._native.build(), OuterStruct)
    
    
    
    class InnerInterface(generated.smoke_OuterStructInnerInterface):
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor; otherwise construct a fresh trampoline. `self._native`
            # aliases the wrapper itself so the rest of the generated code can reach the
            # native object uniformly (e.g. when passing this interface back into a C++
            # call site).
            if native is not None and isinstance(native, generated.smoke_OuterStructInnerInterface):
                super().__init__(native)
            else:
                super().__init__()
            self._native = self
    
        def bar_baz(self) -> dict[str, bytes]:
            return _wrap(generated.smoke_OuterStructInnerInterface.bar_baz(self), dict[str, bytes])
    
    
    
    class InnerEnum(Enum):
    
        FOO = generated.smoke_OuterStructInnerEnum.FOO
        BAR = generated.smoke_OuterStructInnerEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    
    
    class InstantiationError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    TypeAlias = InnerEnum
    
    
    
    InnerLambda = Callable[[], None]
    
    

