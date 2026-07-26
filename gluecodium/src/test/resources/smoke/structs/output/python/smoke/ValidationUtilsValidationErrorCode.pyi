

import typing

from enum import Enum

import generated


class ValidationUtilsValidationErrorCode(Enum):
    """"""

    NONE = generated.smoke_ValidationUtilsValidationErrorCode.NONE
    VALIDATION_FAILED = generated.smoke_ValidationUtilsValidationErrorCode.VALIDATION_FAILED

    @property
    def _native(self):
        return self.value

