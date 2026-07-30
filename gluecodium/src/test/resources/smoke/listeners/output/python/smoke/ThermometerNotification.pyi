

import typing

class ThermometerNotification(Exception):
    """This error indicates problems with notification of observers.
May be thrown if observers cannot be notified."""
    message: str

    def __init__(self, message: str) -> None: ...

