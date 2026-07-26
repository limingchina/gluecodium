

import typing

from enum import Enum

import generated


class SkipEnumeratorExplicitTag(Enum):
    """"""

    ZERO = generated.smoke_SkipEnumeratorExplicitTag.ZERO
    ONE = generated.smoke_SkipEnumeratorExplicitTag.ONE
    THREE = generated.smoke_SkipEnumeratorExplicitTag.THREE

    @property
    def _native(self):
        return self.value

