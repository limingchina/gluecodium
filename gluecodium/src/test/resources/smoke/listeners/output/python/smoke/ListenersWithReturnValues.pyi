

from smoke.CalculationResult import CalculationResult
from smoke.ListenersWithReturnValuesResultEnum import ListenersWithReturnValuesResultEnum
from smoke.ListenersWithReturnValuesResultStruct import ListenersWithReturnValuesResultStruct
import typing

class ListenersWithReturnValues:

    def fetch_data_double(self) -> float:
        ...

    def fetch_data_string(self) -> str:
        ...

    def fetch_data_struct(self) -> ListenersWithReturnValuesResultStruct:
        ...

    def fetch_data_enum(self) -> ListenersWithReturnValuesResultEnum:
        ...

    def fetch_data_array(self) -> list[float]:
        ...

    def fetch_data_map(self) -> dict[str, float]:
        ...

    def fetch_data_instance(self) -> CalculationResult:
        ...

