

import typing

class ThermometerNotification(Exception):
    """This error indicates problems with notification of observers.
May be thrown if observers cannot be notified."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

