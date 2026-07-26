

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class OrderInStructSomeEnum(Enum):
    """"""

    FOO = generated.smoke_OrderInStructSomeEnum.FOO
    BAR = generated.smoke_OrderInStructSomeEnum.BAR

    @property
    def _native(self):
        return self.value

