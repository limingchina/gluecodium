

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class PublicClassInternalEnum(Enum):
    """"""

    FOO = generated.smoke_PublicClassInternalEnum.FOO
    BAR = generated.smoke_PublicClassInternalEnum.BAR

    @property
    def _native(self):
        return self.value

