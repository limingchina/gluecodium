

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class CommentsInterface(generated.smoke_CommentsInterface):
    """This is some very useful interface."""
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("some_method_with_all_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f6457697468416c6c436f6d6d656e7473", "method", None,
             lambda: ([str], bool)),
            ("some_method_with_input_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f6457697468496e707574436f6d6d656e7473", "method", None,
             lambda: ([str], bool)),
            ("some_method_with_output_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684f7574707574436f6d6d656e7473", "method", None,
             lambda: ([str], bool)),
            ("some_method_with_no_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684e6f436f6d6d656e7473", "method", None,
             lambda: ([str], bool)),
            ("some_method_without_return_type_with_all_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e5479706557697468416c6c436f6d6d656e7473", "method", None,
             lambda: ([str], None)),
            ("some_method_without_return_type_with_no_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e54797065576974684e6f436f6d6d656e7473", "method", None,
             lambda: ([str], None)),
            ("some_method_without_input_parameters_with_all_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f7574496e707574506172616d657465727357697468416c6c436f6d6d656e7473", "method", None,
             lambda: ([], bool)),
            ("some_method_without_input_parameters_with_no_comments", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f7574496e707574506172616d6574657273576974684e6f436f6d6d656e7473", "method", None,
             lambda: ([], bool)),
            ("some_method_with_nothing", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684e6f7468696e67", "method", None,
             lambda: ([], None)),
            ("some_method_without_return_type_or_input_parameters", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e547970654f72496e707574506172616d6574657273", "method", None,
             lambda: ([], None)),
            ("is_some_property", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e536f6d6550726f7065727479_get", "get", "is_some_property",
             lambda: ([], bool)),
            ("is_some_property", "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e536f6d6550726f7065727479_set", "set", "set_some_property",
             lambda: ([bool], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_CommentsInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_all_comments(self, _unwrap(input, str)), bool)

    def some_method_with_input_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_input_comments(self, _unwrap(input, str)), bool)

    def some_method_with_output_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_output_comments(self, _unwrap(input, str)), bool)

    def some_method_with_no_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_no_comments(self, _unwrap(input, str)), bool)

    def some_method_without_return_type_with_all_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_return_type_with_all_comments(self, _unwrap(input, str)), None)

    def some_method_without_return_type_with_no_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_return_type_with_no_comments(self, _unwrap(input, str)), None)

    def some_method_without_input_parameters_with_all_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_input_parameters_with_all_comments(self), bool)

    def some_method_without_input_parameters_with_no_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_input_parameters_with_no_comments(self), bool)

    def some_method_with_nothing(self):
        return _wrap(generated.smoke_CommentsInterface.some_method_with_nothing(self), None)

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_return_type_or_input_parameters(self), None)

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(generated.smoke_CommentsInterface.is_some_property.fget(self), bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        """Sets some very useful property."""
        generated.smoke_CommentsInterface.is_some_property.fset(self, _unwrap(value, bool))

    class SomeStruct(_NativeBase):
        """This is some very useful struct."""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CommentsInterface.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_CommentsInterface.SomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> bool:
            """How useful this struct is"""
            return _wrap(self._native.some_field, bool)
        @some_field.setter
        def some_field(self, value: bool):
          self._native.some_field = _unwrap(value, bool)
    
    
    
    
    class SomeEnum(Enum):
        """This is some very useful enum."""
    
        USELESS = generated.smoke_CommentsInterface.SomeEnum.USELESS
        USEFUL = generated.smoke_CommentsInterface.SomeEnum.USEFUL
    
        @property
        def _native(self):
            return self.value
    
    
    
    #: This is some very useful typedef.
    Usefulness = bool
    
    

    #: This is some very useful constant.
    VERY_USEFUL = True

