

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EnumsInternalErrorCode(Enum):
    """"""

    ERROR_NONE = generated.EnumsInternalErrorCode.ERROR_NONE
    ERROR_FATAL = generated.EnumsInternalErrorCode.ERROR_FATAL

    @property
    def _native(self):
        return self.value

