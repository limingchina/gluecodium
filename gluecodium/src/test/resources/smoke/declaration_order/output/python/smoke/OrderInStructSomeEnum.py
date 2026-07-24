

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class OrderInStructSomeEnum(Enum):
    """"""

    FOO = generated.OrderInStructSomeEnum.FOO
    BAR = generated.OrderInStructSomeEnum.BAR

    @property
    def _native(self):
        return self.value

