

from smoke.Thermometer import Thermometer

from _native_base import _NativeBase


class TemperatureObserver(_NativeBase):
    """Observer interface for monitoring changes in thermometer ("Observer of subject")."""

    def __init__(self, native):
        super().__init__(native)


    def on_temperature_update(self, thermometer: Thermometer):
        """"""
        return self._native.on_temperature_update(thermometer)

