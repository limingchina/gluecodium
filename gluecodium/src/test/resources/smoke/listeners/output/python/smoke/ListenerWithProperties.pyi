

from smoke.CalculationResult import CalculationResult
from smoke.ListenerWithPropertiesResultEnum import ListenerWithPropertiesResultEnum
from smoke.ListenerWithPropertiesResultStruct import ListenerWithPropertiesResultStruct
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
    def structured_message(self) -> ListenerWithPropertiesResultStruct:
        ...

    @structured_message.setter
    def structured_message(self, value: ListenerWithPropertiesResultStruct) -> None:
        ...

    @property
    def enumerated_message(self) -> ListenerWithPropertiesResultEnum:
        ...

    @enumerated_message.setter
    def enumerated_message(self, value: ListenerWithPropertiesResultEnum) -> None:
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

