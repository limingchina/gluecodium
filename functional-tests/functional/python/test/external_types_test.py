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

"""External type mapping tests for the Python (pybind11) bindings."""

import functional
from external.ClassWithOverloads import ClassWithOverloads
from external.StandaloneExternalType import StandaloneExternalType

import pytest


class TestExternalTypes:
    def test_class_with_overloads_import(self):
        # Test that the external abstract class can be imported successfully
        # Note: ClassWithOverloads is an abstract class in C++ with only pure virtual methods,
        # so it cannot be instantiated directly in Python
        assert ClassWithOverloads is not None
        assert hasattr(ClassWithOverloads, 'one_overload_not_exposed')
        assert hasattr(ClassWithOverloads, 'all_overloads_exposed')

    def test_standalone_external_type_import(self):
        # Test that the external abstract class can be imported successfully
        # Note: StandaloneExternalType is an abstract class in C++ with a pure virtual method,
        # so it cannot be instantiated directly in Python
        assert StandaloneExternalType is not None
        assert hasattr(StandaloneExternalType, 'foo')
