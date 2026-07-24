

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ExternalEnum3(Enum):
    """"""

    ENABLED = generated.ExternalEnum3.ENABLED
    DISABLED = generated.ExternalEnum3.DISABLED

    @property
    def _native(self):
        return self.value

