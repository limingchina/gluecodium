

from smoke.NullableSomeEnum import NullableSomeEnum
from smoke.NullableSomeStruct import NullableSomeStruct
from smoke.SomeInterface import SomeInterface
import typing

class Nullable:

    def method_with_string(self, input: Optional[str]) -> Optional[str]:
        ...

    def method_with_boolean(self, input: Optional[bool]) -> Optional[bool]:
        ...

    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        ...

    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_some_struct(self, input: Optional[NullableSomeStruct]) -> Optional[NullableSomeStruct]:
        ...

    def method_with_some_enum(self, input: Optional[NullableSomeEnum]) -> Optional[NullableSomeEnum]:
        ...

    def method_with_some_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        ...

    def method_with_inline_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        ...

    def method_with_some_map(self, input: Optional[dict[int, str]]) -> Optional[dict[int, str]]:
        ...

    def method_with_instance(self, input: Optional[SomeInterface]) -> Optional[SomeInterface]:
        ...

    @property
    def string_property(self):
        ...

    @string_property.setter
    def string_property(self, value) -> None:
        ...

    @property
    def is_bool_property(self):
        ...

    @is_bool_property.setter
    def is_bool_property(self, value) -> None:
        ...

    @property
    def double_property(self):
        ...

    @double_property.setter
    def double_property(self, value) -> None:
        ...

    @property
    def int_property(self):
        ...

    @int_property.setter
    def int_property(self, value) -> None:
        ...

    @property
    def struct_property(self):
        ...

    @struct_property.setter
    def struct_property(self, value) -> None:
        ...

    @property
    def enum_property(self):
        ...

    @enum_property.setter
    def enum_property(self, value) -> None:
        ...

    @property
    def array_property(self):
        ...

    @array_property.setter
    def array_property(self, value) -> None:
        ...

    @property
    def inline_array_property(self):
        ...

    @inline_array_property.setter
    def inline_array_property(self, value) -> None:
        ...

    @property
    def map_property(self):
        ...

    @map_property.setter
    def map_property(self, value) -> None:
        ...

    @property
    def instance_property(self):
        ...

    @instance_property.setter
    def instance_property(self, value) -> None:
        ...

