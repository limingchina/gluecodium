

import datetime
from smoke.TemperatureObserver import TemperatureObserver
from smoke.ThermometerAnotherNotification import ThermometerAnotherNotification
from smoke.ThermometerNotification import ThermometerNotification
from smoke.ThermometerSomeThermometerErrorCode import ThermometerSomeThermometerErrorCode
import typing

class Thermometer:
    """A class, which reads temperature and updates observers according to the given interval.
\"Subject\" in observer design pattern."""

    @staticmethod
    def make_with_duration(interval: datetime.timedelta, observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with readout interval."""
        ...

    @staticmethod
    def make_without_duration(observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with default readout interval (1 second)."""
        ...

    @staticmethod
    def throwing_make(id: int, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        ...

    @staticmethod
    def nothrow_make(label: str, nice_observers: list[TemperatureObserver]) -> Thermometer:
        """A non-throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        ...

    @staticmethod
    def another_throwing_make(dummy: bool, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        ...

    @staticmethod
    def notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        ...

    @staticmethod
    def throwing_notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        """Function used to notify observers."""
        ...

    def force_update(self):
        ...

    def get_celsius(self) -> float:
        ...

    def get_kelvin(self) -> float:
        ...

    def get_fahrenheit(self) -> float:
        ...

