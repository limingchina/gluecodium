

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.CalculationResult import CalculationResult
from smoke.ListenerWithPropertiesResultEnum import ListenerWithPropertiesResultEnum
from smoke.ListenerWithPropertiesResultStruct import ListenerWithPropertiesResultStruct


import generated


class ListenerWithProperties(generated.smoke_ListenerWithProperties):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ListenerWithProperties):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @property
    def message(self) -> str:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.message.fget(self), str)

    @message.setter
    def message(self, value: str):
        generated.smoke_ListenerWithProperties.message.fset(self, _unwrap(value, str))

    @property
    def packed_message(self) -> CalculationResult:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.packed_message.fget(self), CalculationResult)

    @packed_message.setter
    def packed_message(self, value: CalculationResult):
        generated.smoke_ListenerWithProperties.packed_message.fset(self, _unwrap(value, CalculationResult))

    @property
    def structured_message(self) -> ListenerWithPropertiesResultStruct:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.structured_message.fget(self), ListenerWithPropertiesResultStruct)

    @structured_message.setter
    def structured_message(self, value: ListenerWithPropertiesResultStruct):
        generated.smoke_ListenerWithProperties.structured_message.fset(self, _unwrap(value, ListenerWithPropertiesResultStruct))

    @property
    def enumerated_message(self) -> ListenerWithPropertiesResultEnum:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.enumerated_message.fget(self), ListenerWithPropertiesResultEnum)

    @enumerated_message.setter
    def enumerated_message(self, value: ListenerWithPropertiesResultEnum):
        generated.smoke_ListenerWithProperties.enumerated_message.fset(self, _unwrap(value, ListenerWithPropertiesResultEnum))

    @property
    def arrayed_message(self) -> list[str]:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.arrayed_message.fget(self), list[str])

    @arrayed_message.setter
    def arrayed_message(self, value: list[str]):
        generated.smoke_ListenerWithProperties.arrayed_message.fset(self, _unwrap(value, list[str]))

    @property
    def mapped_message(self) -> dict[str, float]:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.mapped_message.fget(self), dict[str, float])

    @mapped_message.setter
    def mapped_message(self, value: dict[str, float]):
        generated.smoke_ListenerWithProperties.mapped_message.fset(self, _unwrap(value, dict[str, float]))

    @property
    def buffered_message(self) -> bytes:
        """"""
        return _wrap(generated.smoke_ListenerWithProperties.buffered_message.fget(self), bytes)

    @buffered_message.setter
    def buffered_message(self, value: bytes):
        generated.smoke_ListenerWithProperties.buffered_message.fset(self, _unwrap(value, bytes))

