

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EnumsSimpleEnum(Enum):
    """"""

    FIRST = generated.smoke_EnumsSimpleEnum.FIRST
    SECOND = generated.smoke_EnumsSimpleEnum.SECOND

    @property
    def _native(self):
        return self.value

