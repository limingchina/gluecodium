

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class SkippedEverywhereEnum(Enum):
    """"""

    NOTHING_TO_SEE_HERE = generated.smoke_SkippedEverywhereEnum.NOTHING_TO_SEE_HERE

    @property
    def _native(self):
        return self.value

