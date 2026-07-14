

from __future__ import annotations


from enum import Enum

import generated


class SkipEnumeratorAutoTag(Enum):
    """"""

    ONE = generated.SkipEnumeratorAutoTag.ONE
    THREE = generated.SkipEnumeratorAutoTag.THREE

    @property
    def _native(self):
        return self.value

