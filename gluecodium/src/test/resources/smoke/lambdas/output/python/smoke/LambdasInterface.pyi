

from enum import Enum
import typing
from typing import Callable

class LambdasInterface:

    def take_screenshot(self, callback: Callable[[Optional[bytes]], None]):
        ...

    TakeScreenshotCallback = Callable[[Optional[bytes]], None]
    
    

