

from smoke.CalculationResult import CalculationResult
from smoke.ResultEnum import ResultEnum
from smoke.ResultStruct import ResultStruct
from smoke.dict[str, float] import dict[str, float]


from _native_base import _NativeBase

import generated


class ListenerWithProperties(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ListenerWithProperties):
            super().__init__(native)
        else:
            super().__init__(generated.ListenerWithProperties())


    @property
    def message(self) -> str:
        """"""
        return self._native.message

    @message.setter
    def message(self, value: str):
        self._native.message = value


    @property
    def packed_message(self) -> CalculationResult:
        """"""
        return self._native.packed_message

    @packed_message.setter
    def packed_message(self, value: CalculationResult):
        self._native.packed_message = value


    @property
    def structured_message(self) -> ResultStruct:
        """"""
        return self._native.structured_message

    @structured_message.setter
    def structured_message(self, value: ResultStruct):
        self._native.structured_message = value


    @property
    def enumerated_message(self) -> ResultEnum:
        """"""
        return self._native.enumerated_message

    @enumerated_message.setter
    def enumerated_message(self, value: ResultEnum):
        self._native.enumerated_message = value


    @property
    def arrayed_message(self) -> list[str]:
        """"""
        return self._native.arrayed_message

    @arrayed_message.setter
    def arrayed_message(self, value: list[str]):
        self._native.arrayed_message = value


    @property
    def mapped_message(self) -> dict[str, float]:
        """"""
        return self._native.mapped_message

    @mapped_message.setter
    def mapped_message(self, value: dict[str, float]):
        self._native.mapped_message = value


    @property
    def buffered_message(self) -> bytes:
        """"""
        return self._native.buffered_message

    @buffered_message.setter
    def buffered_message(self, value: bytes):
        self._native.buffered_message = value

