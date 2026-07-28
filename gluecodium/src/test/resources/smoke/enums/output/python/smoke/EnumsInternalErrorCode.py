

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class EnumsInternalErrorCode(Enum):
    """"""

    ERROR_NONE = generated.smoke_EnumsInternalErrorCode.ERROR_NONE
    ERROR_FATAL = generated.smoke_EnumsInternalErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

