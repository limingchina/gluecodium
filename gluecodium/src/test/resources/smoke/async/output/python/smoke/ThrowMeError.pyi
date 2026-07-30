

import typing

class ThrowMeError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

