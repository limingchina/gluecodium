

from smoke.CalculationResult import CalculationResult
from enum import Enum
import typing
from typing import Optional

class ListenersWithReturnValues:

    def fetch_data_double(self) -> float:
        ...

    def fetch_data_string(self) -> str:
        ...

    def fetch_data_struct(self) -> ListenersWithReturnValues.ResultStruct:
        ...

    def fetch_data_enum(self) -> ListenersWithReturnValues.ResultEnum:
        ...

    def fetch_data_array(self) -> list[float]:
        ...

    def fetch_data_map(self) -> dict[str, float]:
        ...

    def fetch_data_instance(self) -> CalculationResult:
        ...

    class ResultStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, result: float) -> None: ...

        result: float



    class ResultEnum(Enum):

        NONE = 0
        RESULT = 1



    StringToDouble = dict[str, float]
