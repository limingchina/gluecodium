

from smoke.ThermometerSomeThermometerErrorCode import ThermometerSomeThermometerErrorCode
import typing

class ThermometerAnotherNotification(Exception):
    """This error indicates other problems with notification of observers."""
    message: str

    def __init__(self, message: str) -> None: ...

