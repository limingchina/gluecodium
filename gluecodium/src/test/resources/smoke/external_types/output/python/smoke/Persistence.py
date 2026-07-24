

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class Persistence(Enum):
    """"""

    NONE = generated.Persistence.NONE
    FOR_SESSION = generated.Persistence.FOR_SESSION
    PERMANENT = generated.Persistence.PERMANENT

    @property
    def _native(self):
        return self.value

