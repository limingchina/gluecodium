

from __future__ import annotations


from enum import Enum

import generated


class SomeSkippedEnum(Enum):
    """"""

    FOO = generated.SomeSkippedEnum.FOO

    @property
    def _native(self):
        return self.value

