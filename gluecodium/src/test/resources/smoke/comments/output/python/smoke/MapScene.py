

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.MapSceneLoadSceneCallback import MapSceneLoadSceneCallback

from _native_base import _NativeBase

import generated


class MapScene(_NativeBase):
    """Referencing some type [MapScene.load_scene(Int, MapScene.LoadSceneCallback?)]."""

    def __init__(self, native):
        super().__init__(native)

    def load_scene(*args, **kwargs):
        """"""
        return _wrap(self._native.load_scene(*[_unwrap(a) for a in args]), None)


