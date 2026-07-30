

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class ValidationUtilsValidationErrorCode(Enum):

    NONE = generated.smoke_ValidationUtilsValidationErrorCode.NONE
    VALIDATION_FAILED = generated.smoke_ValidationUtilsValidationErrorCode.VALIDATION_FAILED

    @property
    def _native(self):
        return self.value

