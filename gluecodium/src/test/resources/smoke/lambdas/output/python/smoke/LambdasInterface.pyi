

from smoke.LambdasInterfaceTakeScreenshotCallback import LambdasInterfaceTakeScreenshotCallback
import typing
from typing import Callable

class LambdasInterface:

    def take_screenshot(self, callback: Callable[[Optional[bytes]], None]):
        ...

