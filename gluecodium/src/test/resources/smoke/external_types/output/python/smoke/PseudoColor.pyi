

import typing


from _native_base import _NativeBase

import generated


class PseudoColor(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PseudoColor):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PseudoColor(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._native == other._native

    def __hash__(self) -> int:
        return hash(self._native)


    @property
    def red(self) -> float:
        """"""
        return _wrap(self._native.red, float)
    @red.setter
    def red(self, value: float):
      self._native.red = _unwrap(value, float)



    @property
    def green(self) -> float:
        """"""
        return _wrap(self._native.green, float)
    @green.setter
    def green(self, value: float):
      self._native.green = _unwrap(value, float)



    @property
    def blue(self) -> float:
        """"""
        return _wrap(self._native.blue, float)
    @blue.setter
    def blue(self, value: float):
      self._native.blue = _unwrap(value, float)



    @property
    def alpha(self) -> float:
        """"""
        return _wrap(self._native.alpha, float)
    @alpha.setter
    def alpha(self, value: float):
      self._native.alpha = _unwrap(value, float)


