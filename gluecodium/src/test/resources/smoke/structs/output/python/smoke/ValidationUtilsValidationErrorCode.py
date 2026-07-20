

from __future__ import annotations


from enum import Enum

import generated


class ValidationUtilsValidationErrorCode(Enum):
    """"""

    NONE = generated.ValidationUtilsValidationErrorCode.NONE
    VALIDATION_FAILED = generated.ValidationUtilsValidationErrorCode.VALIDATION_FAILED

    @property
    def _native(self):
        return self.value

