

from smoke.InnerName import InnerName

from _native_base import _NativeBase


class UseInnerName(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_foo(self) -> InnerName:
        """"""
        return self._native.do_foo()

