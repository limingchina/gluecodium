

from __future__ import annotations


from enum import Enum

import generated


class EnumsSimpleEnum(Enum):
    """"""

    FIRST = generated.EnumsSimpleEnum.FIRST
    SECOND = generated.EnumsSimpleEnum.SECOND

    @property
    def _native(self):
        return self.value

