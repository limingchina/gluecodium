

import typing

from enum import Enum

import generated


class ErrorsInternalErrorCode(Enum):
    """"""

    ERROR_NONE = generated.smoke_ErrorsInternalErrorCode.ERROR_NONE
    ERROR_FATAL = generated.smoke_ErrorsInternalErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

