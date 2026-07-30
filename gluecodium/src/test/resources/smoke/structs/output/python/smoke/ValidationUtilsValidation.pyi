

from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing

class ValidationUtilsValidation(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

