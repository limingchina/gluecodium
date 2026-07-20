

from __future__ import annotations

from smoke.DartInternalClassWithInternalTypedef import DartInternalClassWithInternalTypedef

from _native_base import _NativeBase

import generated


class SomeDartClassThatUsesInternal(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def add_entity(self, entity: DartInternalClassWithInternalTypedef):
        """"""
        return self._native.add_entity(entity._native)

