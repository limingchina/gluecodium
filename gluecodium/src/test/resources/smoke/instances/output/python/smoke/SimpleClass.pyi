

from enum import Enum
import typing
from typing import Optional

class SimpleClass:

    def get_string_value(self) -> str:
        ...

    def use_simple_class(self, input: SimpleClass) -> SimpleClass:
        ...
