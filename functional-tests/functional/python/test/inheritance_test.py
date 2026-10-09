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

"""Inheritance mapping tests for the Python (pybind11) bindings."""

import functional
from test.InheritanceTestHelper import InheritanceTestHelper
from test.RootInterface import RootInterface

import pytest


class TestInheritance:
    def test_create_root(self):
        root = InheritanceTestHelper.create_root()

        assert isinstance(root, RootInterface)

    def test_call_root_method(self):
        root = InheritanceTestHelper.create_root()
        # callRootMethod is void in Lime (it just invokes root_method on the passed
        # object from C++); the real assertion is that no pure-virtual error is raised.
        InheritanceTestHelper.call_root_method(root, "data")

        assert isinstance(root, RootInterface)

    def test_create_concrete_grand_child(self):
        child = InheritanceTestHelper.create_concrete_grand_child()

        assert child is not None
