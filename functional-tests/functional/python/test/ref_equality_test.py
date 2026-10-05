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

"""Reference equality tests for the Python (pybind11) bindings."""

import functional
from test.DummyFactory import DummyFactory
from test.DummyClass import DummyClass

import pytest
import subprocess
import sys


@pytest.mark.parametrize("parent_first", [True, False])
def test_child_wrapper_identity_across_parent_views(parent_first):
    # Each process starts with an empty identity cache, making access order observable.
    script = f"""
from test.DummyFactory import DummyFactory
from test.DummyChildClass import DummyChildClass
if {parent_first!r}:
    parent = DummyFactory.get_dummy_child_class_singleton_as_parent()
    child = DummyFactory.get_dummy_child_class_singleton()
else:
    child = DummyFactory.get_dummy_child_class_singleton()
    parent = DummyFactory.get_dummy_child_class_singleton_as_parent()
assert isinstance(parent, DummyChildClass)
assert isinstance(child, DummyChildClass)
assert parent is child
"""
    subprocess.run([sys.executable, "-c", script], check=True, timeout=10)


@pytest.mark.parametrize("parent_first", [True, False])
def test_child_interface_identity_across_parent_views(parent_first):
    script = f"""
from test.DummyFactory import DummyFactory
from test.DummyChildInterface import DummyChildInterface
if {parent_first!r}:
    parent = DummyFactory.get_dummy_child_interface_singleton_as_parent()
    child = DummyFactory.get_dummy_child_interface_singleton()
else:
    child = DummyFactory.get_dummy_child_interface_singleton()
    parent = DummyFactory.get_dummy_child_interface_singleton_as_parent()
assert isinstance(parent, DummyChildInterface)
assert isinstance(child, DummyChildInterface)
assert parent is child
"""
    subprocess.run([sys.executable, "-c", script], check=True, timeout=10)


class TestRefEquality:
    def test_singleton_is_same_instance(self):
        first = DummyFactory.get_dummy_class_singleton()
        second = DummyFactory.get_dummy_class_singleton()

        assert first is second

    def test_created_instances_differ(self):
        first = DummyFactory.create_dummy_class()
        second = DummyFactory.create_dummy_class()

        assert first is not second

    def test_round_trip_preserves_identity(self):
        original = DummyFactory.get_dummy_class_singleton()
        result = DummyClass.dummy_class_round_trip(original)

        assert result is original
