

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional
from typing import Callable

from smoke.LambdasInterfaceTakeScreenshotCallback import LambdasInterfaceTakeScreenshotCallback


import generated


class LambdasInterface(generated.LambdasInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.LambdasInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def take_screenshot(self, callback: Callable[[Optional[bytes]], None]):
        """"""
        return _wrap(generated.LambdasInterface.take_screenshot(self, _unwrap(callback, Callable[[Optional[bytes]], None])), None)

