

from smoke.Thermometer import Thermometer
import typing

class TemperatureObserver:
    """Observer interface for monitoring changes in thermometer (\"Observer of subject\")."""

    def on_temperature_update(self, thermometer: Thermometer):
        ...

