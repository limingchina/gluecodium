

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class PublicClassInternalEnum(Enum):
    """"""

    FOO = generated.PublicClassInternalEnum.FOO
    BAR = generated.PublicClassInternalEnum.BAR

    @property
    def _native(self):
        return self.value

