

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class PlatformCommentsSomeEnum(Enum):
    """"""

    USELESS = generated.smoke_PlatformCommentsSomeEnum.USELESS
    USEFUL = generated.smoke_PlatformCommentsSomeEnum.USEFUL

    @property
    def _native(self):
        return self.value

