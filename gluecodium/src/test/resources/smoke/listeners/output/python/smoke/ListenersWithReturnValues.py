

from __future__ import annotations

from smoke.CalculationResult import CalculationResult
from smoke.ListenersWithReturnValuesResultStruct import ListenersWithReturnValuesResultStruct
from smoke.ResultEnum import ResultEnum


from _native_base import _NativeBase

import generated


class ListenersWithReturnValues(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ListenersWithReturnValues):
            super().__init__(native)
        else:
            super().__init__(generated.ListenersWithReturnValues())

    def fetch_data_double(self) -> float:
        """"""
        return self._native.fetch_data_double()

    def fetch_data_string(self) -> str:
        """"""
        return self._native.fetch_data_string()

    def fetch_data_struct(self) -> ListenersWithReturnValuesResultStruct:
        """"""
        return self._native.fetch_data_struct()

    def fetch_data_enum(self) -> ResultEnum:
        """"""
        return self._native.fetch_data_enum()

    def fetch_data_array(self) -> list[float]:
        """"""
        return self._native.fetch_data_array()

    def fetch_data_map(self) -> dict[str, float]:
        """"""
        return self._native.fetch_data_map()

    def fetch_data_instance(self) -> CalculationResult:
        """"""
        return self._native.fetch_data_instance()
from enum import Enum


class ResultEnum(Enum):
    """"""

    NONE = 0
    RESULT = 1


