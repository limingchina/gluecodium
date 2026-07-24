

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


class ThermometerNotification(Exception):
    """This error indicates problems with notification of observers.
May be thrown if observers cannot be notified."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

