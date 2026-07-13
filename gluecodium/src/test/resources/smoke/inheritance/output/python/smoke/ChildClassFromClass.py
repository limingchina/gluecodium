

from __future__ import annotations

from smoke.ParentClass import ParentClass


from _native_base import _NativeBase

import generated


class ChildClassFromClass(
    ParentClass)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def child_class_method(self):
        """"""
        return self._native.child_class_method()

