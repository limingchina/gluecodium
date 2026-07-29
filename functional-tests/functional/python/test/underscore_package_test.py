# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""Underscore package name tests for the Python (pybind11) bindings.

Verifies that a LIME package name containing an underscore (``test_off``)
is preserved as-is in the generated Python module path, with no case
conversion or other name mangling.
"""

import functional
from test_off.OffInterface import OffInterface
from test_off.OffStruct import OffStruct
from test.UseUnderscorePackage import UseUnderscorePackage

import pytest


class TestUnderscorePackage:
    def test_import_underscore_package(self):
        """The underscore package ``test_off`` must be importable as-is."""
        # If the import at the top of this file succeeded, the package path
        # was preserved correctly. Verify the types are usable.
        assert OffInterface is not None
        assert OffStruct is not None

    def test_instantiate_struct_from_underscore_package(self):
        struct = OffStruct(struct_field="hello")
        assert struct.struct_field == "hello"

    def test_method_with_underscore_struct(self):
        """Round-trip a struct through a method that uses the underscore package."""
        input_struct = OffStruct(struct_field="data")
        result = UseUnderscorePackage.method_with_underscore_struct(input_struct)

        assert isinstance(result, OffStruct)
        # The C++ implementation returns a default-constructed OffStruct,
        # so struct_field is an empty string.
        assert result.struct_field == ""

    def test_method_with_underscore_instance(self):
        """The static method that uses the underscore-package class must be callable.

        ``OffInterface`` has no user-defined constructor, so it cannot be
        instantiated directly from Python. The C++ binding accepts ``None``
        (a null ``shared_ptr``) for the parameter, and returns ``nullptr``.
        """
        result = UseUnderscorePackage.method_with_underscore_instance(None)

        # The C++ implementation returns nullptr.
        assert result is None
