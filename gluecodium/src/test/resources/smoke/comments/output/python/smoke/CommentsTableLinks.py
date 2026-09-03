

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class CommentsTableLinks(_NativeBase):
    """Something lorem something ipsum.

| Tables | Are | Cool |
|----------|:-------------:|------:|
| col 1 is |  `CommentsTable` | $1600 |
| col 2 is |`Comments.SomeEnum`|   $12 |
| col 3 is |`Comments.SomeEnum.USEFUL`|    $1 |"""
    def __init__(self, native):
        super().__init__(native)


