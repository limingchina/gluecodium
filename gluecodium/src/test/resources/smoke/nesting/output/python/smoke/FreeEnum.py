

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class FreeEnum(Enum):
    """"""

    FOO = generated.smoke_FreeEnum.FOO
    BAR = generated.smoke_FreeEnum.BAR

    @property
    def _native(self):
        return self.value

