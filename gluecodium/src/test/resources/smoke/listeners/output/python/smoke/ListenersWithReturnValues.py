

from smoke.CalculationResult import CalculationResult
from smoke.ResultEnum import ResultEnum
from smoke.ResultStruct import ResultStruct
from smoke.dict[str, float] import dict[str, float]

class ListenersWithReturnValues:
    """"""

    def __init__(self, native):
        self._native = native


    def fetch_data_double(self) -> float:
        """"""
        return self._native.fetch_data_double()


    def fetch_data_string(self) -> str:
        """"""
        return self._native.fetch_data_string()


    def fetch_data_struct(self) -> ResultStruct:
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

