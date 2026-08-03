

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

import datetime
from smoke.TemperatureObserver import TemperatureObserver

class Thermometer(_NativeBase):
    """A class, which reads temperature and updates observers according to the given interval.
\"Subject\" in observer design pattern."""
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make_with_duration(interval: datetime.timedelta, observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with readout interval."""
        native_result = generated.smoke_Thermometer.make_with_duration(_unwrap(interval, datetime.timedelta), _unwrap(observers, list[TemperatureObserver]))
        return _get_or_create_wrapper(native_result, Thermometer)

    @staticmethod
    def make_without_duration(observers: list[TemperatureObserver]) -> Thermometer:
        """A constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.smoke_Thermometer.make_without_duration(_unwrap(observers, list[TemperatureObserver]))
        return _get_or_create_wrapper(native_result, Thermometer)

    @staticmethod
    def throwing_make(id: int, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.smoke_Thermometer.throwing_make(_unwrap(id, int), _unwrap(observers, list[TemperatureObserver]))
        return _get_or_create_wrapper(native_result, Thermometer)

    @staticmethod
    def nothrow_make(label: str, nice_observers: list[TemperatureObserver]) -> Thermometer:
        """A non-throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.smoke_Thermometer.nothrow_make(_unwrap(label, str), _unwrap(nice_observers, list[TemperatureObserver]))
        return _get_or_create_wrapper(native_result, Thermometer)

    @staticmethod
    def another_throwing_make(dummy: bool, observers: list[TemperatureObserver]) -> Thermometer:
        """A throwing constructor, which makes the thermometer with default readout interval (1 second)."""
        native_result = generated.smoke_Thermometer.another_throwing_make(_unwrap(dummy, bool), _unwrap(observers, list[TemperatureObserver]))
        return _get_or_create_wrapper(native_result, Thermometer)

    @staticmethod
    def notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        generated.smoke_Thermometer.notify_observers(_unwrap(thermometer, Thermometer), _unwrap(some_observers, list[TemperatureObserver]))

    @staticmethod
    def throwing_notify_observers(thermometer: Thermometer, some_observers: list[TemperatureObserver]):
        """Function used to notify observers."""
        generated.smoke_Thermometer.throwing_notify_observers(_unwrap(thermometer, Thermometer), _unwrap(some_observers, list[TemperatureObserver]))

    def force_update(self):
        return _wrap(self._native.force_update(), None)

    def get_celsius(self) -> float:
        return _wrap(self._native.get_celsius(), float)

    def get_kelvin(self) -> float:
        return _wrap(self._native.get_kelvin(), float)

    def get_fahrenheit(self) -> float:
        return _wrap(self._native.get_fahrenheit(), float)

    class SomeThermometerErrorCode(Enum):
        """Some error code for thermometer."""
    
        ERROR_NONE = generated.smoke_Thermometer.SomeThermometerErrorCode.ERROR_NONE
        ERROR_FATAL = generated.smoke_Thermometer.SomeThermometerErrorCode.ERROR_FATAL
    
        @property
        def _native(self):
            return self.value
    
    
    
    class NotificationError(Exception):
        """This error indicates problems with notification of observers.
    May be thrown if observers cannot be notified."""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    class AnotherNotificationError(Exception):
        """This error indicates other problems with notification of observers."""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

