

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ListenerInterface(generated.smoke_ListenerInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ListenerInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def notify(self):
        return _wrap(generated.smoke_ListenerInterface.notify(self), None)


