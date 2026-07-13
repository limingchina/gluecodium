

from __future__ import annotations



from _native_base import _NativeBase

import generated


class AsyncWithSkips(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def make_shared_instance(android_context: str):
        """"""
        native_result = generated.AsyncWithSkips.make_shared_instance(android_context)
        return None(native_result)

    @staticmethod

    def make_shared_instance():
        """"""
        native_result = generated.AsyncWithSkips.make_shared_instance()
        return None(native_result)

