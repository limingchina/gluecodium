

from smoke.OuterStruct import OuterStruct
import typing

class OuterStructBuilder:

    @staticmethod
    def create() -> OuterStructBuilder:
        ...

    def field(self, value: str) -> OuterStructBuilder:
        ...

    def build(self) -> OuterStruct:
        ...

