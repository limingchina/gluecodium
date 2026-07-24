

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.DartInternalClassWithInternalTypedef import DartInternalClassWithInternalTypedef

from _native_base import _NativeBase

import generated


class SomeDartClassThatUsesInternal(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def add_entity(self, entity: DartInternalClassWithInternalTypedef):
        """"""
        return _wrap(self._native.add_entity(_unwrap(entity, DartInternalClassWithInternalTypedef)), None)

