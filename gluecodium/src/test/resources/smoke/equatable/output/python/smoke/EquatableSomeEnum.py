

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EquatableSomeEnum(Enum):
    """"""

    FOO = generated.smoke_EquatableSomeEnum.FOO
    BAR = generated.smoke_EquatableSomeEnum.BAR

    @property
    def _native(self):
        return self.value

