

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class Enum2(Enum):

    ENABLED = generated.fire_Enum2.ENABLED
    DISABLED = generated.fire_Enum2.DISABLED

    @property
    def _native(self):
        return self.value

