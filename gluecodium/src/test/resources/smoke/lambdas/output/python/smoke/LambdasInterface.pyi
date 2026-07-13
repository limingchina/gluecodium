

from smoke.TakeScreenshotCallback import TakeScreenshotCallback

from _native_base import _NativeBase


class LambdasInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def take_screenshot(self, callback: TakeScreenshotCallback):
        """"""
        return self._native.take_screenshot(callback)

