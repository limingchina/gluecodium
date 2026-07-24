

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class CommentsTable(_NativeBase):
    """Something lorem something ipsum.

| Tables | Are | Cool |
|----------|:-------------:|------:|
| col 1 is |  left-aligned | $1600 |
| col 2 is |    centered   |   $12 |
| col 3 is | right-aligned |    $1 |"""

    def __init__(self, native):
        super().__init__(native)

