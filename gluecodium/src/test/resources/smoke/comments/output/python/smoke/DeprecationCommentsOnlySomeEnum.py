

from __future__ import annotations


from enum import Enum

import generated


class DeprecationCommentsOnlySomeEnum(Enum):
    """"""

    USELESS = generated.DeprecationCommentsOnlySomeEnum.USELESS

    @property
    def _native(self):
        return self.value

