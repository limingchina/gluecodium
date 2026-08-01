

from smoke.CalculationResult import CalculationResult
from enum import Enum
import typing

class ListenerWithProperties:

    @property
    def message(self) -> str:
        ...

    @message.setter
    def message(self, value: str) -> None:
        ...

    @property
    def packed_message(self) -> CalculationResult:
        ...

    @packed_message.setter
    def packed_message(self, value: CalculationResult) -> None:
        ...

    @property
    def structured_message(self) -> ListenerWithProperties.ResultStruct:
        ...

    @structured_message.setter
    def structured_message(self, value: ListenerWithProperties.ResultStruct) -> None:
        ...

    @property
    def enumerated_message(self) -> ListenerWithProperties.ResultEnum:
        ...

    @enumerated_message.setter
    def enumerated_message(self, value: ListenerWithProperties.ResultEnum) -> None:
        ...

    @property
    def arrayed_message(self) -> list[str]:
        ...

    @arrayed_message.setter
    def arrayed_message(self, value: list[str]) -> None:
        ...

    @property
    def mapped_message(self) -> dict[str, float]:
        ...

    @mapped_message.setter
    def mapped_message(self, value: dict[str, float]) -> None:
        ...

    @property
    def buffered_message(self) -> bytes:
        ...

    @buffered_message.setter
    def buffered_message(self, value: bytes) -> None:
        ...

    class ResultStruct:
    
        result: float
    
    
    
    class ResultEnum(Enum):
    
        NONE = 0
        RESULT = 1
    
    
    
    dict[str, float] = dict[str, float]
    
    

