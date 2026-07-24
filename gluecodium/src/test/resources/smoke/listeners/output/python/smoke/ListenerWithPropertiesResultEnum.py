

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class ListenerWithPropertiesResultEnum(Enum):
    """"""

    NONE = generated.ListenerWithPropertiesResultEnum.NONE
    RESULT = generated.ListenerWithPropertiesResultEnum.RESULT

    @property
    def _native(self):
        return self.value

