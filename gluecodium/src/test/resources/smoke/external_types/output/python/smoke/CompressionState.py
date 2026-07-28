

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class CompressionState(Enum):
    """"""

    COMPRESSED = generated.smoke_CompressionState.COMPRESSED
    DECOMPRESSED = generated.smoke_CompressionState.DECOMPRESSED
    NOT_COMPRESSED = generated.smoke_CompressionState.NOT_COMPRESSED

    @property
    def _native(self):
        return self.value

