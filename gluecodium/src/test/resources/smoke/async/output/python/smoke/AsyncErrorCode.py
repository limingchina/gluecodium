

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class AsyncErrorCode(Enum):
    """"""

    VALUE1 = generated.AsyncErrorCode.VALUE1

    @property
    def _native(self):
        return self.value

