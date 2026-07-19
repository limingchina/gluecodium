



from _native_base import _NativeBase

import generated


class DartColor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DartColor):
            super().__init__(args[0])
        else:
            super().__init__(generated.DartColor(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def red(self) -> float:
        """"""
        return self._native.red
    @red.setter
    def red(self, value: float):
      self._native.red = getattr(value, "_native", value)



    @property
    def green(self) -> float:
        """"""
        return self._native.green
    @green.setter
    def green(self, value: float):
      self._native.green = getattr(value, "_native", value)



    @property
    def blue(self) -> float:
        """"""
        return self._native.blue
    @blue.setter
    def blue(self, value: float):
      self._native.blue = getattr(value, "_native", value)



    @property
    def alpha(self) -> float:
        """"""
        return self._native.alpha
    @alpha.setter
    def alpha(self, value: float):
      self._native.alpha = getattr(value, "_native", value)


