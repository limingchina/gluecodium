

import typing

from enum import Enum

import generated


class PropertiesInternalErrorCode(Enum):
    """"""

    ERROR_NONE = generated.smoke_PropertiesInternalErrorCode.ERROR_NONE
    ERROR_FATAL = generated.smoke_PropertiesInternalErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

