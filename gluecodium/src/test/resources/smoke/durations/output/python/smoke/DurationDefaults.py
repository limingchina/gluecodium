

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DurationDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DurationDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DurationDefaults(*args))


    @property
    def dayz(self) -> datetime.timedelta:
        """"""
        return self._native.dayz

    @dayz.setter
    def dayz(self, value: datetime.timedelta):
        self._native.dayz = value



    @property
    def hourz(self) -> datetime.timedelta:
        """"""
        return self._native.hourz

    @hourz.setter
    def hourz(self, value: datetime.timedelta):
        self._native.hourz = value



    @property
    def minutez(self) -> datetime.timedelta:
        """"""
        return self._native.minutez

    @minutez.setter
    def minutez(self, value: datetime.timedelta):
        self._native.minutez = value



    @property
    def secondz(self) -> datetime.timedelta:
        """"""
        return self._native.secondz

    @secondz.setter
    def secondz(self, value: datetime.timedelta):
        self._native.secondz = value



    @property
    def milliz(self) -> datetime.timedelta:
        """"""
        return self._native.milliz

    @milliz.setter
    def milliz(self, value: datetime.timedelta):
        self._native.milliz = value



    @property
    def microz(self) -> datetime.timedelta:
        """"""
        return self._native.microz

    @microz.setter
    def microz(self, value: datetime.timedelta):
        self._native.microz = value



    @property
    def nanoz(self) -> datetime.timedelta:
        """"""
        return self._native.nanoz

    @nanoz.setter
    def nanoz(self, value: datetime.timedelta):
        self._native.nanoz = value


