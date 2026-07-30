

import typing

class EquatableStructWithAccessors:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    foo_field: str

