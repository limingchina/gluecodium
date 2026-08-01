

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Month(Enum):

    JANUARY = generated.smoke_Month.JANUARY
    FEBRUARY = generated.smoke_Month.FEBRUARY
    MARCH = generated.smoke_Month.MARCH

    @property
    def _native(self):
        return self.value


