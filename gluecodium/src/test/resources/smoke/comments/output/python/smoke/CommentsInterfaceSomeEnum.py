

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class CommentsInterfaceSomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = generated.smoke_CommentsInterfaceSomeEnum.USELESS
    USEFUL = generated.smoke_CommentsInterfaceSomeEnum.USEFUL

    @property
    def _native(self):
        return self.value

