

import typing

from enum import Enum

import generated


class PropertiesInternalErrorCode(Enum):
    """"""

    ERROR_NONE = generated.PropertiesInternalErrorCode.ERROR_NONE
    ERROR_FATAL = generated.PropertiesInternalErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

