

from __future__ import annotations



from _native_base import _NativeBase

import generated


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

    @staticmethod

    def make(result: str) -> SpecialNames:
        """"""
        native_result = generated.SpecialNames.make(result)
        return SpecialNames(native_result)

