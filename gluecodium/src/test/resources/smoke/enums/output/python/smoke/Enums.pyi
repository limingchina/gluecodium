

from smoke.EnumsErrorStruct import EnumsErrorStruct
from smoke.EnumsInternalErrorCode import EnumsInternalErrorCode
from smoke.EnumsSimpleEnum import EnumsSimpleEnum
import typing

class Enums:

    @staticmethod
    def method_with_enumeration(input: EnumsSimpleEnum) -> EnumsSimpleEnum:
        ...

    @staticmethod
    def flip_enum_value(input: EnumsInternalErrorCode) -> EnumsInternalErrorCode:
        ...

    @staticmethod
    def extract_enum_from_struct(input: EnumsErrorStruct) -> EnumsInternalErrorCode:
        ...

    @staticmethod
    def create_struct_with_enum_inside(type: EnumsInternalErrorCode, message: str) -> EnumsErrorStruct:
        ...

