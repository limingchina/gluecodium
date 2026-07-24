

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class SomethingEnum(Enum):
    """"""

    REALLY_FIRST = generated.SomethingEnum.REALLY_FIRST
    EXPLICIT = generated.SomethingEnum.EXPLICIT
    LAST = generated.SomethingEnum.LAST

    @property
    def _native(self):
        return self.value

