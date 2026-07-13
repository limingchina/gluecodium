

from smoke.CalculationResult import CalculationResult
from smoke.ResultEnum import ResultEnum
from smoke.ResultStruct import ResultStruct
from smoke.dict[str, float] import dict[str, float]

class ListenerWithProperties:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def message(self) -> str:
        """"""
        return self._native.message



    @property
    def packed_message(self) -> CalculationResult:
        """"""
        return self._native.packed_message



    @property
    def structured_message(self) -> ResultStruct:
        """"""
        return self._native.structured_message



    @property
    def enumerated_message(self) -> ResultEnum:
        """"""
        return self._native.enumerated_message



    @property
    def arrayed_message(self) -> list[str]:
        """"""
        return self._native.arrayed_message



    @property
    def mapped_message(self) -> dict[str, float]:
        """"""
        return self._native.mapped_message



    @property
    def buffered_message(self) -> bytes:
        """"""
        return self._native.buffered_message


