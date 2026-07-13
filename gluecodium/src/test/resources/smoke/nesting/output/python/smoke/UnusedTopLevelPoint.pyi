



from _native_base import _NativeBase

import generated


class UnusedTopLevelPoint(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], UnusedTopLevelPoint):
            super().__init__(args[0])
        else:
            super().__init__(generated.UnusedTopLevelPoint(*args))


    @property
    def foo(self) -> str:
        """"""
        return self._native.foo

    @foo.setter
    def foo(self, value: str):
        self._native.foo = value


