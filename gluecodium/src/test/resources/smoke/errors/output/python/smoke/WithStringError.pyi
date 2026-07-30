

import typing

class WithStringError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

