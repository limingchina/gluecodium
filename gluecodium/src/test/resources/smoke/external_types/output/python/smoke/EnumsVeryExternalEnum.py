

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class EnumsVeryExternalEnum(Enum):
    """"""

    FOO = generated.smoke_EnumsVeryExternalEnum.FOO
    BAR = generated.smoke_EnumsVeryExternalEnum.BAR

    @property
    def _native(self):
        return self.value

