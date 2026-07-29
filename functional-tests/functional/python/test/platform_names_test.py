# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""@Python(Name=...) platform-name override tests for the Python (pybind11) bindings.

Verifies that every element type (struct, class, interface, enum, method, field,
property, constructor, parameter, enumerator) honours the ``@Python(Name = ...)``
attribute, ensuring the Python name resolver respects platform-specific naming.
"""

import functional
from test.QuxEnum import QuxEnum
from test.QuxInterface import QuxInterface
from test.QuxListener import QuxListener
from test.QuxStruct import QuxStruct
from test.QuxTypes import QuxTypes

import pytest


class TestPlatformNames:
    # --- Type names ---

    def test_struct_type_renamed(self):
        """Top-level struct ``PlatformNames`` is exposed as ``QuxTypes``."""
        assert QuxTypes is not None
        assert QuxTypes.__name__ == "QuxTypes"

    def test_nested_struct_type_renamed(self):
        """Nested struct ``BasicStruct`` is exposed as ``QuxStruct``."""
        assert QuxStruct is not None
        assert QuxStruct.__name__ == "QuxStruct"

    def test_enum_type_renamed(self):
        """Nested enum ``BasicEnum`` is exposed as ``QuxEnum``."""
        assert QuxEnum is not None
        assert QuxEnum.__name__ == "QuxEnum"

    def test_class_type_renamed(self):
        """Class ``PlatformNamesInterface`` is exposed as ``QuxInterface``."""
        assert QuxInterface is not None
        assert QuxInterface.__name__ == "QuxInterface"

    def test_interface_type_renamed(self):
        """Interface ``PlatformNamesListener`` is exposed as ``QuxListener``."""
        assert QuxListener is not None
        assert QuxListener.__name__ == "QuxListener"

    # --- Enumerator names ---

    def test_enumerator_renamed(self):
        """Enumerator ``BASIC_ITEM`` is exposed as ``QUX_ITEM``."""
        assert hasattr(QuxEnum, "QUX_ITEM")
        assert not hasattr(QuxEnum, "BASIC_ITEM")

    # --- Field names ---

    def test_struct_field_renamed(self):
        """Field ``stringField`` is exposed as ``qux_field``."""
        instance = QuxStruct(qux_field="hello")
        assert hasattr(instance, "qux_field")
        assert not hasattr(instance, "string_field")
        assert instance.qux_field == "hello"

    # --- Constructor names ---

    def test_struct_factory_constructor_renamed(self):
        """Static factory ``make`` on the struct is exposed as ``qux_make``."""
        assert hasattr(QuxStruct, "qux_make")
        result = QuxStruct.qux_make(qux_parameter="test")
        assert isinstance(result, QuxStruct)

    def test_class_constructor_renamed(self):
        """Constructor ``create`` on the class is exposed as ``qux_create``."""
        assert hasattr(QuxInterface, "qux_create")
        instance = QuxInterface.qux_create(make_parameter="some_string")
        assert isinstance(instance, QuxInterface)

    # --- Method names ---

    def test_static_method_renamed(self):
        """Static method ``basicMethod`` is exposed as ``qux_method``."""
        assert hasattr(QuxInterface, "qux_method")
        assert not hasattr(QuxInterface, "basic_method")

    def test_static_method_returns_renamed_struct(self):
        result = QuxInterface.qux_method(qux_parameter="input")
        assert isinstance(result, QuxStruct)

    # --- Property names ---

    def test_property_renamed(self):
        """Property ``basicAttribute`` is exposed as ``qux_attribute``."""
        instance = QuxInterface.qux_create(make_parameter="some_string")
        assert hasattr(instance, "qux_attribute")
        assert not hasattr(instance, "basic_attribute")

    def test_property_get_and_set(self):
        """Property ``qux_attribute`` round-trips a value."""
        instance = QuxInterface.qux_create(make_parameter="some_string")
        instance.qux_attribute = 77
        assert instance.qux_attribute == 77

    # --- Interface method names ---

    def test_interface_method_renamed(self):
        """Interface method ``basicMethod`` is exposed as ``qux_method``."""
        assert hasattr(QuxListener, "qux_method")
        assert not hasattr(QuxListener, "basic_method")

    def test_interface_implementation(self):
        """A Python subclass of ``QuxListener`` can override ``qux_method``."""

        class MyListener(QuxListener):
            def __init__(self):
                super().__init__()
                self.received = None

            def qux_method(self, qux_parameter: str):
                self.received = qux_parameter

        listener = MyListener()
        listener.qux_method(qux_parameter="from_python")
        assert listener.received == "from_python"
