

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class InternalClassWithComments(_NativeBase):
    """This looks internal"""

    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self):
        """This is definitely internal"""
        return _wrap(self._native.do_nothing(), None)

