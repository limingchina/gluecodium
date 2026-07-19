

from smoke.CalculationResult import CalculationResult
from smoke.ListenerWithPropertiesResultEnum import ListenerWithPropertiesResultEnum
from smoke.ListenerWithPropertiesResultStruct import ListenerWithPropertiesResultStruct


import generated


class ListenerWithProperties(generated.ListenerWithProperties):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ListenerWithProperties):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @property
    def message(self) -> str:
        """"""
        return generated.ListenerWithProperties.message.fget(self)

    @message.setter
    def message(self, value: str):
        generated.ListenerWithProperties.message.fset(self, value)

    @property
    def packed_message(self) -> CalculationResult:
        """"""
        return generated.ListenerWithProperties.packed_message.fget(self)

    @packed_message.setter
    def packed_message(self, value: CalculationResult):
        generated.ListenerWithProperties.packed_message.fset(self, value)

    @property
    def structured_message(self) -> ListenerWithPropertiesResultStruct:
        """"""
        return generated.ListenerWithProperties.structured_message.fget(self)

    @structured_message.setter
    def structured_message(self, value: ListenerWithPropertiesResultStruct):
        generated.ListenerWithProperties.structured_message.fset(self, value)

    @property
    def enumerated_message(self) -> ListenerWithPropertiesResultEnum:
        """"""
        return generated.ListenerWithProperties.enumerated_message.fget(self)

    @enumerated_message.setter
    def enumerated_message(self, value: ListenerWithPropertiesResultEnum):
        generated.ListenerWithProperties.enumerated_message.fset(self, value)

    @property
    def arrayed_message(self) -> list[str]:
        """"""
        return generated.ListenerWithProperties.arrayed_message.fget(self)

    @arrayed_message.setter
    def arrayed_message(self, value: list[str]):
        generated.ListenerWithProperties.arrayed_message.fset(self, value)

    @property
    def mapped_message(self) -> dict[str, float]:
        """"""
        return generated.ListenerWithProperties.mapped_message.fget(self)

    @mapped_message.setter
    def mapped_message(self, value: dict[str, float]):
        generated.ListenerWithProperties.mapped_message.fset(self, value)

    @property
    def buffered_message(self) -> bytes:
        """"""
        return generated.ListenerWithProperties.buffered_message.fget(self)

    @buffered_message.setter
    def buffered_message(self, value: bytes):
        generated.ListenerWithProperties.buffered_message.fset(self, value)

