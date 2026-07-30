

from namerules.NameRulesExampleErrorCode import NameRulesExampleErrorCode
import typing

class NameRulesExample(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

