

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class Annotations(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def test_optional(self, self: Annotations) -> Optional[bool]:
        """"""
        return _wrap(self._native.test_optional(_unwrap(self, Annotations)), Optional[bool])

