

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class SimpleInterface(generated.smoke_SimpleInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("get_string_value", "__gluecodium_callback_736d6f6b652e53696d706c65496e746572666163652e676574537472696e6756616c7565", "method", None,
             lambda: ([], str)),
            ("use_simple_interface", "__gluecodium_callback_736d6f6b652e53696d706c65496e746572666163652e75736553696d706c65496e74657266616365", "method", None,
             lambda: ([SimpleInterface], SimpleInterface)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_SimpleInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def get_string_value(self) -> str:
        return _wrap(generated.smoke_SimpleInterface.get_string_value(self), str)

    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        return _wrap(generated.smoke_SimpleInterface.use_simple_interface(self, _unwrap(input, SimpleInterface)), SimpleInterface)
