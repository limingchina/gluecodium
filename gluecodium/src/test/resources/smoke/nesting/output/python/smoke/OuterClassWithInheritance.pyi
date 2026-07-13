

from smoke.ParentClass import ParentClass


from _native_base import _NativeBase

import generated


class OuterClassWithInheritance(
    ParentClass)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self, input: str) -> str:
        """"""
        return self._native.foo(input)

