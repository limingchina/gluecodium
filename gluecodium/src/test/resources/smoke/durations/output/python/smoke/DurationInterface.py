

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime


import generated


class DurationInterface(generated.smoke_DurationInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_DurationInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def duration_function(self, input: datetime.timedelta) -> str:
        """"""
        return _wrap(generated.smoke_DurationInterface.duration_function(self, _unwrap(input, datetime.timedelta)), str)

