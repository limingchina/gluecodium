

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class DeprecationCommentsSomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = generated.DeprecationCommentsSomeEnum.USELESS

    @property
    def _native(self):
        return self.value

