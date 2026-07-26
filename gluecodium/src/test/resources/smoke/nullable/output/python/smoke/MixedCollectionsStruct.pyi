

import datetime
import typing


from _native_base import _NativeBase

import generated


class MixedCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_MixedCollectionsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_MixedCollectionsStruct(*[_unwrap(arg) for arg in args]))


    @property
    def almost_dates(self) -> list[Optional[datetime.datetime]]:
        """"""
        return _wrap(self._native.almost_dates, list[Optional[datetime.datetime]])
    @almost_dates.setter
    def almost_dates(self, value: list[Optional[datetime.datetime]]):
      self._native.almost_dates = _unwrap(value, list[Optional[datetime.datetime]])



    @property
    def dates(self) -> list[datetime.datetime]:
        """"""
        return _wrap(self._native.dates, list[datetime.datetime])
    @dates.setter
    def dates(self, value: list[datetime.datetime]):
      self._native.dates = _unwrap(value, list[datetime.datetime])


