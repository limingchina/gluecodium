

from smoke.ThermometerSomeThermometerErrorCode import ThermometerSomeThermometerErrorCode
import typing

class ThermometerAnotherNotification(Exception):
    """This error indicates other problems with notification of observers."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

