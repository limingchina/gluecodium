

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ListenersWithReturnValuesResultEnum(Enum):
    """"""

    NONE = generated.ListenersWithReturnValuesResultEnum.NONE
    RESULT = generated.ListenersWithReturnValuesResultEnum.RESULT

    @property
    def _native(self):
        return self.value

