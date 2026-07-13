

from __future__ import annotations

from smoke.LoadSceneCallback import LoadSceneCallback


from _native_base import _NativeBase

import generated


class MapScene(_NativeBase):
    """Referencing some type [MapScene.load_scene(Int, MapScene.LoadSceneCallback?)]."""

    def __init__(self, native):
        super().__init__(native)


    def load_scene(self, map_scheme: int, callback: Optional[LoadSceneCallback]):
        """"""
        return self._native.load_scene(map_scheme, callback._native)


    def load_scene(self, configuration_file: str, callback: Optional[LoadSceneCallback]):
        """"""
        return self._native.load_scene(configuration_file, callback._native)

