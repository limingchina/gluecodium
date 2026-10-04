

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class LambdasInterface(generated.smoke_LambdasInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_LambdasInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def take_screenshot(self, callback: Callable[[Optional[bytes]], None]):
        return _wrap(generated.smoke_LambdasInterface.take_screenshot(self, _unwrap(callback, Callable[[Optional[bytes]], None])), None)

    TakeScreenshotCallback = Callable[[Optional[bytes]], None]
    
    

