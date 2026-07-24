

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EnumOptionSetComments(Enum):
    """"""

    ONE = generated.EnumOptionSetComments.ONE
    TWO = generated.EnumOptionSetComments.TWO
    THREE = generated.EnumOptionSetComments.THREE

    @property
    def _native(self):
        return self.value

