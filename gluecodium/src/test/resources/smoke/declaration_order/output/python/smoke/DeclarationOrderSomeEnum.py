

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class DeclarationOrderSomeEnum(Enum):
    """"""

    FOO = generated.smoke_DeclarationOrderSomeEnum.FOO
    BAR = generated.smoke_DeclarationOrderSomeEnum.BAR

    @property
    def _native(self):
        return self.value

