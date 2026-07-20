

from __future__ import annotations


from enum import Enum

import generated


class PlatformCommentsSomeEnum(Enum):
    """"""

    USELESS = generated.PlatformCommentsSomeEnum.USELESS
    USEFUL = generated.PlatformCommentsSomeEnum.USEFUL

    @property
    def _native(self):
        return self.value

