

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class SomeInternalEnum(Enum):
    """"""

    ONE = generated.smoke_SomeInternalEnum.ONE
    TWO = generated.smoke_SomeInternalEnum.TWO
    THREE = generated.smoke_SomeInternalEnum.THREE
    SINGLE = generated.smoke_SomeInternalEnum.SINGLE

    @property
    def _native(self):
        return self.value

