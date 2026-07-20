

from smoke.MapSceneLoadSceneCallback import MapSceneLoadSceneCallback
import typing

from _native_base import _NativeBase

import generated


class MapScene(_NativeBase):
    """Referencing some type [MapScene.load_scene(Int, MapScene.LoadSceneCallback?)]."""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    def load_scene(self, map_scheme: int, callback: Optional[MapSceneLoadSceneCallback]): ...

    @typing.overload
    def load_scene(self, configuration_file: str, callback: Optional[MapSceneLoadSceneCallback]): ...

