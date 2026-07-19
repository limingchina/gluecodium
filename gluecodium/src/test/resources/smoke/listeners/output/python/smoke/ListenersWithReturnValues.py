

from __future__ import annotations

from smoke.CalculationResult import CalculationResult
from smoke.ListenersWithReturnValuesResultEnum import ListenersWithReturnValuesResultEnum
from smoke.ListenersWithReturnValuesResultStruct import ListenersWithReturnValuesResultStruct


import generated


class ListenersWithReturnValues(generated.ListenersWithReturnValues):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ListenersWithReturnValues):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def fetch_data_double(self) -> float:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_double(self)

    def fetch_data_string(self) -> str:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_string(self)

    def fetch_data_struct(self) -> ListenersWithReturnValuesResultStruct:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_struct(self)

    def fetch_data_enum(self) -> ListenersWithReturnValuesResultEnum:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_enum(self)

    def fetch_data_array(self) -> list[float]:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_array(self)

    def fetch_data_map(self) -> dict[str, float]:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_map(self)

    def fetch_data_instance(self) -> CalculationResult:
        """"""
        return generated.ListenersWithReturnValues.fetch_data_instance(self)

