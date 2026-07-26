

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class CppRefReturnTypeInternalError(Enum):
    """"""

    FOO = generated.smoke_CppRefReturnTypeInternalError.FOO
    BAR = generated.smoke_CppRefReturnTypeInternalError.BAR

    @property
    def _native(self):
        return self.value

