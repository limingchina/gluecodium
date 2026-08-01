

from smoke.CompressionState import CompressionState
from smoke.Rectangle import Rectangle
from enum import Enum
import typing

class UseDartExternalGenerics:

    def use_generics(self, list: list[Rectangle], set: set[CompressionState]) -> dict[CompressionState, Rectangle]:
        ...


