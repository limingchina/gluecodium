

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class StructsFooBar(Enum):
    """"""

    FOO = generated.StructsFooBar.FOO
    BAR = generated.StructsFooBar.BAR

    @property
    def _native(self):
        return self.value

