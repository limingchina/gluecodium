

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
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
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStruct.InnerStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_OuterStruct.InnerStruct(
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
            native_result = generated.smoke_OuterStruct.Builder.create()
            return _get_or_create_wrapper(native_result, OuterStruct.Builder)
    
        def field(self, value: str) -> OuterStruct.Builder:
            return _wrap(self._native.field(_unwrap(value, str)), OuterStruct.Builder)
    
        def build(self) -> OuterStruct:
            return _wrap(self._native.build(), OuterStruct)
    
    
    
    @_mark_callback_base
    class InnerInterface(generated.smoke_OuterStruct.InnerInterface):
        @classmethod
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            _install_callback_adapters(cls, __class__, [
                ("bar_baz", "__gluecodium_callback_736d6f6b652e4f757465725374727563742e496e6e6572496e746572666163652e62617242617a", "method", None,
                 lambda: ([], dict[str, bytes])),
            ])
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor and retain the original native object for calls back into
            # C++; otherwise construct a fresh trampoline.
            if native is not None and isinstance(native, generated.smoke_OuterStruct.InnerInterface):
                super().__init__(native)
                self._native = native
            else:
                super().__init__()
                self._native = self
    
        def bar_baz(self) -> dict[str, bytes]:
            return _wrap(generated.smoke_OuterStruct.InnerInterface.bar_baz(self), dict[str, bytes])
    
    
    
    class InnerEnum(Enum):
    
        FOO = generated.smoke_OuterStruct.InnerEnum.FOO
        BAR = generated.smoke_OuterStruct.InnerEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    
    
    class InstantiationError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    TypeAlias = InnerEnum
    
    
    
    InnerLambda = Callable[[], None]
    
    

