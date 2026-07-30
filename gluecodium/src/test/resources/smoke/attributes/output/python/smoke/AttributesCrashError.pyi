

import typing

class AttributesCrashError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

