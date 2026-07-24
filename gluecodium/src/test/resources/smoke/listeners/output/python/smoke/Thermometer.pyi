

import datetime
from smoke.TemperatureObserver import TemperatureObserver
from smoke.ThermometerAnotherNotification import ThermometerAnotherNotification
from smoke.ThermometerNotification import ThermometerNotification
from smoke.ThermometerSomeThermometerErrorCode import ThermometerSomeThermometerErrorCode
import typing

from _native_base import _NativeBase

import generated


class Thermometer(_NativeBase):
    """A class, which reads temperature and updates observers according to the given interval.
\"Subject\" in observer design pattern."""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make_with_duration(interval: datetime.timedelta, observers: list[TemperatureObserver]) -> Thermometer: ...

    @staticmethod
    def make_without_duration(observers: list[TemperatureObserver]) -> Thermometer: ...

    @staticmethod
    def throwing_make(id: int, observers: list[TemperatureObserver]) -> Thermometer: ...

    @staticmethod
    def nothrow_make(label: str, nice_observers: list[TemperatureObserver]) -> Thermometer: ...

    @staticmethod
    def another_throwing_make(dummy: bool, observers: list[TemperatureObserver]) -> Thermometer: ...

    @staticmethod
    def notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]): ...

    @staticmethod
    def throwing_notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]): ...

    def force_update(self): ...

    def get_celsius(self) -> float: ...

    def get_kelvin(self) -> float: ...

    def get_fahrenheit(self) -> float: ...

