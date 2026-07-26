

import typing

from enum import Enum

import generated


class ThermometerSomeThermometerErrorCode(Enum):
    """Some error code for thermometer."""

    ERROR_NONE = generated.smoke_ThermometerSomeThermometerErrorCode.ERROR_NONE
    ERROR_FATAL = generated.smoke_ThermometerSomeThermometerErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

