

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class EnumsInTypeCollectionTCEnum(Enum):
    """"""

    FIRST = generated.smoke_EnumsInTypeCollectionTCEnum.FIRST
    SECOND = generated.smoke_EnumsInTypeCollectionTCEnum.SECOND

    @property
    def _native(self):
        return self.value

