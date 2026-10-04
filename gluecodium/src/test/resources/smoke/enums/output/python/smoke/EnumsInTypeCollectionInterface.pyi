

from smoke.EnumsInTypeCollection import EnumsInTypeCollection
from enum import Enum
import typing
from typing import Optional

class EnumsInTypeCollectionInterface:

    @staticmethod
    def flip_enum_value(input: EnumsInTypeCollection.TCEnum) -> EnumsInTypeCollection.TCEnum:
        ...
