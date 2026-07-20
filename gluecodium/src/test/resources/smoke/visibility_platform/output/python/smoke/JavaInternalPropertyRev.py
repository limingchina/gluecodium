

from __future__ import annotations


from _native_base import _NativeBase

import generated


class JavaInternalPropertyRev(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @property
    def app_context(self):
        """"""
        return self._native.app_context

    @app_context.setter
    def app_context(self, value):
        self._native.app_context = value

