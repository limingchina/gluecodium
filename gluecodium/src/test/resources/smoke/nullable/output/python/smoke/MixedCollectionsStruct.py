

from __future__ import annotations



from _native_base import _NativeBase

import generated


class MixedCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], MixedCollectionsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.MixedCollectionsStruct(*args))


    @property
    def almost_dates(self) -> list[Optional[datetime.datetime]]:
        """"""
        return self._native.almost_dates

    @almost_dates.setter
    def almost_dates(self, value: list[Optional[datetime.datetime]]):
        self._native.almost_dates = value



    @property
    def dates(self) -> list[datetime.datetime]:
        """"""
        return self._native.dates

    @dates.setter
    def dates(self, value: list[datetime.datetime]):
        self._native.dates = value


