

import datetime
import typing


from _native_base import _NativeBase

import generated


class DurationDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DurationDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DurationDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def dayz(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.dayz, datetime.timedelta)
    @dayz.setter
    def dayz(self, value: datetime.timedelta):
      self._native.dayz = _unwrap(value, datetime.timedelta)



    @property
    def hourz(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.hourz, datetime.timedelta)
    @hourz.setter
    def hourz(self, value: datetime.timedelta):
      self._native.hourz = _unwrap(value, datetime.timedelta)



    @property
    def minutez(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.minutez, datetime.timedelta)
    @minutez.setter
    def minutez(self, value: datetime.timedelta):
      self._native.minutez = _unwrap(value, datetime.timedelta)



    @property
    def secondz(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.secondz, datetime.timedelta)
    @secondz.setter
    def secondz(self, value: datetime.timedelta):
      self._native.secondz = _unwrap(value, datetime.timedelta)



    @property
    def milliz(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.milliz, datetime.timedelta)
    @milliz.setter
    def milliz(self, value: datetime.timedelta):
      self._native.milliz = _unwrap(value, datetime.timedelta)



    @property
    def microz(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.microz, datetime.timedelta)
    @microz.setter
    def microz(self, value: datetime.timedelta):
      self._native.microz = _unwrap(value, datetime.timedelta)



    @property
    def nanoz(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.nanoz, datetime.timedelta)
    @nanoz.setter
    def nanoz(self, value: datetime.timedelta):
      self._native.nanoz = _unwrap(value, datetime.timedelta)


