

import typing

from _native_base import _NativeBase

import generated


class JavaInternalPropertyRev(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @property
    def app_context(self):
        """"""
        return _wrap(self._native.app_context, Optional[str])

    @app_context.setter
    def app_context(self, value):
        self._native.app_context = _unwrap(value, Optional[str])

