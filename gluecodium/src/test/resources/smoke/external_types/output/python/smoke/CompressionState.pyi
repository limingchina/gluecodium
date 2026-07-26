

import typing

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

