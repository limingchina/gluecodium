

from smoke.SpecialNames import SpecialNames

from _native_base import _NativeBase


class SpecialNames(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def create(self):
        """"""
        return self._native.create()


    def release(self):
        """"""
        return self._native.release()


    def create_proxy(self):
        """"""
        return self._native.create_proxy()


    def _uppercase(self):
        """"""
        return self._native._uppercase()


    def make(self, result: str) -> SpecialNames:
        """"""
        return self._native.make(result)

