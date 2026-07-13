

from smoke.TakeScreenshotCallback import TakeScreenshotCallback

class LambdasInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def take_screenshot(self, callback: TakeScreenshotCallback):
        """"""
        return self._native.take_screenshot(callback)

