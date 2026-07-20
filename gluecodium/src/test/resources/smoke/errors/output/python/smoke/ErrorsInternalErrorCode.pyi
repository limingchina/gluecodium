

import typing

from enum import Enum

import generated


class ErrorsInternalErrorCode(Enum):
    """"""

    ERROR_NONE = generated.ErrorsInternalErrorCode.ERROR_NONE
    ERROR_FATAL = generated.ErrorsInternalErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

