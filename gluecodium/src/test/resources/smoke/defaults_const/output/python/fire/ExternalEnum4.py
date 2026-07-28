

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class ExternalEnum4(Enum):
    """"""

    ENABLED = generated.fire_ExternalEnum4.ENABLED
    DISABLED = generated.fire_ExternalEnum4.DISABLED

    @property
    def _native(self):
        return self.value

