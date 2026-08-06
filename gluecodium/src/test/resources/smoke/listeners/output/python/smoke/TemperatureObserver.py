

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class TemperatureObserver(generated.smoke_TemperatureObserver):
    """Observer interface for monitoring changes in thermometer (\"Observer of subject\")."""
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_TemperatureObserver):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def on_temperature_update(self, thermometer: Thermometer):
        return _wrap(generated.smoke_TemperatureObserver.on_temperature_update(self, _unwrap(thermometer, Thermometer)), None)


from smoke.Thermometer import Thermometer
