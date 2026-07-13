

from __future__ import annotations

from smoke.TakeScreenshotCallback import TakeScreenshotCallback


from _native_base import _NativeBase

import generated


class LambdasInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, LambdasInterface):
            super().__init__(native)
        else:
            super().__init__(generated.LambdasInterface())


    def take_screenshot(self, callback: TakeScreenshotCallback):
        """"""
        return self._native.take_screenshot(callback._native)

