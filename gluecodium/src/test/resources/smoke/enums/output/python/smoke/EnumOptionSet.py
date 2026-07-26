

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EnumOptionSet(Enum):
    """"""

    ONE = generated.smoke_EnumOptionSet.ONE
    TWO = generated.smoke_EnumOptionSet.TWO
    THREE = generated.smoke_EnumOptionSet.THREE

    @property
    def _native(self):
        return self.value

