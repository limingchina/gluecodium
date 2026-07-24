

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ValidationUtilsValidationErrorCode(Enum):
    """"""

    NONE = generated.ValidationUtilsValidationErrorCode.NONE
    VALIDATION_FAILED = generated.ValidationUtilsValidationErrorCode.VALIDATION_FAILED

    @property
    def _native(self):
        return self.value

