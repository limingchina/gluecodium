

from enum import Enum
import typing
from typing import Optional

class CompressionState(Enum):

    COMPRESSED = 0
    DECOMPRESSED = 1
    NOT_COMPRESSED = 2
