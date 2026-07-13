

from smoke.Thermometer import Thermometer


from _native_base import _NativeBase

import generated


class TemperatureObserver(_NativeBase):
    """Observer interface for monitoring changes in thermometer ("Observer of subject")."""

    def __init__(self, native=None):
        if isinstance(native, TemperatureObserver):
            super().__init__(native)
        else:
            super().__init__(generated.TemperatureObserver())


    def on_temperature_update(self, thermometer: Thermometer):
        """"""
        return self._native.on_temperature_update(thermometer._native)

