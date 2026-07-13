



from _native_base import _NativeBase

import generated


class SystemColor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SystemColor):
            super().__init__(args[0])
        else:
            super().__init__(generated.SystemColor(*args))


    @property
    def red(self) -> float:
        """"""
        return self._native.red

    @red.setter
    def red(self, value: float):
        self._native.red = value



    @property
    def green(self) -> float:
        """"""
        return self._native.green

    @green.setter
    def green(self, value: float):
        self._native.green = value



    @property
    def blue(self) -> float:
        """"""
        return self._native.blue

    @blue.setter
    def blue(self, value: float):
        self._native.blue = value



    @property
    def alpha(self) -> float:
        """"""
        return self._native.alpha

    @alpha.setter
    def alpha(self, value: float):
        self._native.alpha = value


