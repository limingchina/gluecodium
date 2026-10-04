

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ListenerInterface import ListenerInterface

class Weakling(generated.smoke_Weakling):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_Weakling):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    @property
    def listener(self):
        return _wrap(generated.smoke_Weakling.listener.fget(self), Optional[ListenerInterface])

    @listener.setter
    def listener(self, value):
        generated.smoke_Weakling.listener.fset(self, _unwrap(value, Optional[ListenerInterface]))


