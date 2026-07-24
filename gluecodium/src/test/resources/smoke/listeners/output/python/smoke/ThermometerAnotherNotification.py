

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ThermometerSomeThermometerErrorCode import ThermometerSomeThermometerErrorCode

class ThermometerAnotherNotification(Exception):
    """This error indicates other problems with notification of observers."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

