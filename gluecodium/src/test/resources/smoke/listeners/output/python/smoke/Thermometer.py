

from __future__ import annotations

import datetime
from smoke.AnotherNotificationError import AnotherNotificationError
from smoke.NotificationError import NotificationError
from smoke.SomeThermometerErrorCode import SomeThermometerErrorCode


from _native_base import _NativeBase

import generated


class Thermometer(_NativeBase):
    """A class, which reads temperature and updates observers according to the given interval.
"Subject" in observer design pattern."""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    A constructor, which makes the thermometer with readout interval.
    def make_with_duration(interval: datetime.timedelta, observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with readout interval."""
        native_result = generated.Thermometer.make_with_duration(interval, observers)
        return Thermometer(native_result)

    @staticmethod
    A constructor, which makes the thermometer with default readout interval (1 second).
    def make_without_duration(observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.Thermometer.make_without_duration(observers)
        return Thermometer(native_result)

    @staticmethod
    A throwing constructor, which makes the thermometer with default readout interval (1 second).
    def throwing_make(id: int, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.Thermometer.throwing_make(id, observers)
        return Thermometer(native_result)

    @staticmethod
    A non-throwing constructor, which makes the thermometer with default readout interval (1 second).
    def nothrow_make(label: str, nice_observers: list[TemperatureObserver]) -> Thermometer:
        """A non-throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.Thermometer.nothrow_make(label, nice_observers)
        return Thermometer(native_result)

    @staticmethod
    A throwing constructor, which makes the thermometer with default readout interval (1 second).
    def another_throwing_make(dummy: bool, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.Thermometer.another_throwing_make(dummy, observers)
        return Thermometer(native_result)

    @staticmethod

    def notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        """"""
        native_result = generated.Thermometer.notify_observers(thermometer, some_observers)
        return None(native_result)

    @staticmethod
    Function used to notify observers.
    def throwing_notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        """Function used to notify observers."""
        native_result = generated.Thermometer.throwing_notify_observers(thermometer, some_observers)
        return None(native_result)


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

from enum import Enum


class SomeThermometerErrorCode(Enum):
    """Some error code for thermometer."""

    ERROR_NONE = 0
    ERROR_FATAL = 1

