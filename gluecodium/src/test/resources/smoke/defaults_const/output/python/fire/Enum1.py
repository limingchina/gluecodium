

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class Enum1(Enum):
    """"""

    ENABLED = generated.Enum1.ENABLED
    DISABLED = generated.Enum1.DISABLED

    @property
    def _native(self):
        return self.value

