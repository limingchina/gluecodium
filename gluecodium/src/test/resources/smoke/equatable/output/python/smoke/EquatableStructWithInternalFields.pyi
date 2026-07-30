

import typing

class EquatableStructWithInternalFields:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    public_field: str

