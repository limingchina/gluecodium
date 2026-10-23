

from enum import Enum
import typing
from typing import Optional

class SimpleInterface:

    def get_string_value(self) -> str:
        ...

    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        ...
