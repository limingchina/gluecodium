

from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor
from enum import Enum
import typing

class ChildWithCustomConstructor(
    ParentWithCustomConstructor):

    @staticmethod
    def make() -> ChildWithCustomConstructor:
        ...


