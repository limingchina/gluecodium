

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ThermometerSomeThermometerErrorCode(Enum):
    """Some error code for thermometer."""

    ERROR_NONE = generated.ThermometerSomeThermometerErrorCode.ERROR_NONE
    ERROR_FATAL = generated.ThermometerSomeThermometerErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

