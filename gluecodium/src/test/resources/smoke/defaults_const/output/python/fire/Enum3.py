

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class Enum3(Enum):
    """"""

    ENABLED = generated.Enum3.ENABLED
    DISABLED = generated.Enum3.DISABLED

    @property
    def _native(self):
        return self.value

