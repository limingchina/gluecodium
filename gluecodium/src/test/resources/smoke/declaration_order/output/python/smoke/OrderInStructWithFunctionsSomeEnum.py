

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class OrderInStructWithFunctionsSomeEnum(Enum):
    """"""

    FOO = generated.OrderInStructWithFunctionsSomeEnum.FOO
    BAR = generated.OrderInStructWithFunctionsSomeEnum.BAR

    @property
    def _native(self):
        return self.value

