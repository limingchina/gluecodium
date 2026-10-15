

from smoke.Thermometer import Thermometer
from enum import Enum
import typing
from typing import Optional

class TemperatureObserver:
    """Observer interface for monitoring changes in thermometer (\"Observer of subject\")."""

    def on_temperature_update(self, thermometer: Thermometer):
        ...
