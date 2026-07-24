

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class OuterStructInnerEnum(Enum):
    """"""

    FOO = generated.OuterStructInnerEnum.FOO
    BAR = generated.OuterStructInnerEnum.BAR

    @property
    def _native(self):
        return self.value

