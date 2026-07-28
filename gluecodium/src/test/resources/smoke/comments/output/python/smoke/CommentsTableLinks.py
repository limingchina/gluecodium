

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class CommentsTableLinks(_NativeBase):
    """Something lorem something ipsum.

| Tables | Are | Cool |
|----------|:-------------:|------:|
| col 1 is |  [CommentsTable] | $1600 |
| col 2 is |[comments.SomeEnum]|   $12 |
| col 3 is |[comments.SomeEnum.USEFUL]|    $1 |"""

    def __init__(self, native):
        super().__init__(native)

