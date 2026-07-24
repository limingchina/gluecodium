

from namerules.NameRulesExampleErrorCode import NameRulesExampleErrorCode
import typing

class NameRulesExample(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

