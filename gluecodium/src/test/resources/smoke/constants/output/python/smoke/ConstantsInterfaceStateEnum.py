

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ConstantsInterfaceStateEnum(Enum):
    """"""

    OFF = generated.ConstantsInterfaceStateEnum.OFF
    ON = generated.ConstantsInterfaceStateEnum.ON

    @property
    def _native(self):
        return self.value

