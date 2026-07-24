

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.NestedReferencesNestedReferences import NestedReferencesNestedReferences

from _native_base import _NativeBase

import generated


class NestedReferences(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def inside_out(self, struct1: NestedReferencesNestedReferences, struct2: NestedReferencesNestedReferences) -> NestedReferences:
        """"""
        return _wrap(self._native.inside_out(_unwrap(struct1, NestedReferencesNestedReferences), _unwrap(struct2, NestedReferencesNestedReferences)), NestedReferences)

