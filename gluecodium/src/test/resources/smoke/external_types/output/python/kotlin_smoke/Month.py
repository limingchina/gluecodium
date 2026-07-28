

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class Month(Enum):
    """"""

    JANUARY = generated.kotlin_smoke_Month.JANUARY
    FEBRUARY = generated.kotlin_smoke_Month.FEBRUARY
    MARCH = generated.kotlin_smoke_Month.MARCH

    @property
    def _native(self):
        return self.value

