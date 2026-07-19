



from _native_base import _NativeBase

import generated


class SkipOverloads(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SkipOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipOverloads(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def dummy(self) -> float:
        """"""
        return self._native.dummy
    @dummy.setter
    def dummy(self, value: float):
      self._native.dummy = getattr(value, "_native", value)


    def do_foo(self, input: float):
        """"""
        return self._native.do_foo(input)

