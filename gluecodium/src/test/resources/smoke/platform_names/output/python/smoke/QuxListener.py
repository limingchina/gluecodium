

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class QuxListener(generated.smoke_QuxListener):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("qux_method", "__gluecodium_callback_736d6f6b652e506c6174666f726d4e616d65734c697374656e65722e62617369634d6574686f64", "method", None,
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_QuxListener):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def qux_method(self, qux_parameter: str):
        return _wrap(generated.smoke_QuxListener.qux_method(self, _unwrap(qux_parameter, str)), None)
