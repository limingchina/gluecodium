

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class SkipEnumeratorAutoTag(Enum):

    ONE = generated.smoke_SkipEnumeratorAutoTag.ONE
    THREE = generated.smoke_SkipEnumeratorAutoTag.THREE

    @property
    def _native(self):
        return self.value

