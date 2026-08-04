

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke._DartInternalClassWithInternalTypedef import _DartInternalClassWithInternalTypedef

class SomeDartClassThatUsesInternal(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def _add_entity(self, entity: _DartInternalClassWithInternalTypedef):
        """"""
        return _wrap(self._native._add_entity(_unwrap(entity, _DartInternalClassWithInternalTypedef)), None)

    _ListOfInternals = list[_DartInternalClassWithInternalTypedef]
    
    

