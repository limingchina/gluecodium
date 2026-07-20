

from __future__ import annotations

from smoke.MapSceneLoadSceneCallback import MapSceneLoadSceneCallback

from _native_base import _NativeBase

import generated


class MapScene(_NativeBase):
    """Referencing some type [MapScene.load_scene(Int, MapScene.LoadSceneCallback?)]."""

    def __init__(self, native):
        super().__init__(native)

    def load_scene(*args, **kwargs):
        """"""
        return self._native.load_scene(*[getattr(a, "_native", a) for a in args])


