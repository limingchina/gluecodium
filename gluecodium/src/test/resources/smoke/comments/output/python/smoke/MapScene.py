

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class MapScene(_NativeBase):
    """Referencing some type `MapScene.load_scene`."""
    def __init__(self, native):
        super().__init__(native)

    def load_scene(self, *args, **kwargs):
        return _wrap(self._native.load_scene(*[_unwrap(a) for a in args]), None)


    LoadSceneCallback = Callable[[Optional[str]], None]
    
    

