

from smoke.Thermometer import Thermometer

class TemperatureObserver:
    """Observer interface for monitoring changes in thermometer ("Observer of subject")."""

    def __init__(self, native):
        self._native = native


    def on_temperature_update(self, thermometer: Thermometer):
        """"""
        return self._native.on_temperature_update(thermometer)

