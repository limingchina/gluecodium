

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.CalculatorListener import CalculatorListener

class Calculator(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def register_listener(listener: CalculatorListener):
        generated.smoke_Calculator.register_listener(_unwrap(listener, CalculatorListener))

    @staticmethod
    def unregister_listener(listener: CalculatorListener):
        generated.smoke_Calculator.unregister_listener(_unwrap(listener, CalculatorListener))
