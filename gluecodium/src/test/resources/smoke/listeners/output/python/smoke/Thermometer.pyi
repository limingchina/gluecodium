

import datetime
from smoke.AnotherNotificationError import AnotherNotificationError
from smoke.NotificationError import NotificationError
from smoke.SomeThermometerErrorCode import SomeThermometerErrorCode
from smoke.Thermometer import Thermometer

from _native_base import _NativeBase


class Thermometer(_NativeBase):
    """A class, which reads temperature and updates observers according to the given interval.
"Subject" in observer design pattern."""

    def __init__(self, native):
        super().__init__(native)

    A constructor, which makes the thermometer with readout interval.
    def make_with_duration(self, interval: datetime.timedelta, observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with readout interval."""
        return self._native.make_with_duration(interval, observers)

    A constructor, which makes the thermometer with default readout interval (1 second).
    def make_without_duration(self, observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with default readout interval (1 second)."""
        return self._native.make_without_duration(observers)

    A throwing constructor, which makes the thermometer with default readout interval (1 second).
    def throwing_make(self, id: int, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        return self._native.throwing_make(id, observers)

    A non-throwing constructor, which makes the thermometer with default readout interval (1 second).
    def nothrow_make(self, label: str, nice_observers: list[TemperatureObserver]) -> Thermometer:
        """A non-throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        return self._native.nothrow_make(label, nice_observers)

    A throwing constructor, which makes the thermometer with default readout interval (1 second).
    def another_throwing_make(self, dummy: bool, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        return self._native.another_throwing_make(dummy, observers)


    def notify_observers(self, thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        """"""
        return self._native.notify_observers(thermometer, some_observers)

    Function used to notify observers.
    def throwing_notify_observers(self, thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        """Function used to notify observers."""
        return self._native.throwing_notify_observers(thermometer, some_observers)


    def force_update(self):
        """"""
        return self._native.force_update()


    def get_celsius(self) -> float:
        """"""
        return self._native.get_celsius()


    def get_kelvin(self) -> float:
        """"""
        return self._native.get_kelvin()


    def get_fahrenheit(self) -> float:
        """"""
        return self._native.get_fahrenheit()

