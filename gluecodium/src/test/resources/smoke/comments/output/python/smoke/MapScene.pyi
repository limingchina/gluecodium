

from enum import Enum
import typing
from typing import Callable

class MapScene:
    """Referencing some type `MapScene.load_scene`."""

    def load_scene(self, map_scheme: int, callback: Optional[Callable[[Optional[str]], None]]):
        ...

    def load_scene(self, configuration_file: str, callback: Optional[Callable[[Optional[str]], None]]):
        ...

    LoadSceneCallback = Callable[[Optional[str]], None]
    
    

