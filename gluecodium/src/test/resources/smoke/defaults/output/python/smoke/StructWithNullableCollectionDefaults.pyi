



from _native_base import _NativeBase

import generated


class StructWithNullableCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithNullableCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithNullableCollectionDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def nullable_list_field(self):
        """"""
        return self._native.nullable_list_field

    @nullable_list_field.setter
    def nullable_list_field(self, value):
      self._native.nullable_list_field = getattr(value, "_native", value)



    @property
    def nullable_map_field(self):
        """"""
        return self._native.nullable_map_field

    @nullable_map_field.setter
    def nullable_map_field(self, value):
      self._native.nullable_map_field = getattr(value, "_native", value)



    @property
    def nullable_set_field(self):
        """"""
        return self._native.nullable_set_field

    @nullable_set_field.setter
    def nullable_set_field(self, value):
      self._native.nullable_set_field = getattr(value, "_native", value)


