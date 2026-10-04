

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class ExternalInterface(generated.smoke_ExternalInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("some_method", "__gluecodium_callback_736d6f6b652e45787465726e616c496e746572666163652e736f6d655f4d6574686f64", "method", None,
             lambda: ([int], None)),
            ("some_property", "__gluecodium_callback_736d6f6b652e45787465726e616c496e746572666163652e736f6d655f50726f7065727479_get", "get", "get_Me",
             lambda: ([], str)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ExternalInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def some_method(self, some_parameter: int):
        return _wrap(generated.smoke_ExternalInterface.some_method(self, _unwrap(some_parameter, int)), None)

    @property
    def some_property(self) -> str:
        return _wrap(generated.smoke_ExternalInterface.some_property.fget(self), str)


    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalInterface.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExternalInterface.SomeStruct(
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
    
        SOME_VALUE = generated.smoke_ExternalInterface.SomeEnum.SOME_VALUE
    
        @property
        def _native(self):
            return self.value
    
    

