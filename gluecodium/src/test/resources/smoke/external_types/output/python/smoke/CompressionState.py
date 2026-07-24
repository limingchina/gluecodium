

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class CompressionState(Enum):
    """"""

    COMPRESSED = generated.CompressionState.COMPRESSED
    DECOMPRESSED = generated.CompressionState.DECOMPRESSED
    NOT_COMPRESSED = generated.CompressionState.NOT_COMPRESSED

    @property
    def _native(self):
        return self.value

