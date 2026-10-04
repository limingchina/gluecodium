

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class QuxListener(generated.smoke_QuxListener):
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


