

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class OrderInClassSomeEnum(Enum):
    """"""

    FOO = generated.OrderInClassSomeEnum.FOO
    BAR = generated.OrderInClassSomeEnum.BAR

    @property
    def _native(self):
        return self.value

