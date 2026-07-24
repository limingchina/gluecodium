

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class SkipEnumeratorExplicitTag(Enum):
    """"""

    ZERO = generated.SkipEnumeratorExplicitTag.ZERO
    ONE = generated.SkipEnumeratorExplicitTag.ONE
    THREE = generated.SkipEnumeratorExplicitTag.THREE

    @property
    def _native(self):
        return self.value

