

from smoke.MapSceneLoadSceneCallback import MapSceneLoadSceneCallback
import typing
from typing import Callable

class MapScene:
    """Referencing some type [MapScene.load_scene(Int, MapScene.LoadSceneCallback?)]."""

    def load_scene(self, map_scheme: int, callback: Optional[Callable[[Optional[str]], None]]):
        ...

    def load_scene(self, configuration_file: str, callback: Optional[Callable[[Optional[str]], None]]):
        ...

