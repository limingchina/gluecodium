

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ExternalEnum2(Enum):
    """"""

    ENABLED = generated.fire_ExternalEnum2.ENABLED
    DISABLED = generated.fire_ExternalEnum2.DISABLED

    @property
    def _native(self):
        return self.value

