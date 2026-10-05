# Copyright (C) 2016-2026 HERE Europe B.V.
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

"""Identity caching preserves live wrappers without owning native resources."""

import gc
import subprocess
import sys
import weakref

import pytest

from test.DummyClass import DummyClass
from test.DummyFactory import DummyFactory
from test.MultipleInheritanceFactory import MultipleInheritanceFactory
from _native_base import _wrapper_cache


@pytest.mark.parametrize('factory', [DummyFactory.create_dummy_class, DummyFactory.create_dummy_interface])
def test_wrapper_cache_does_not_own_returned_object(factory):
    value = factory()
    reference = weakref.ref(value)
    key = (value._native.__gluecodium_id__(), None)
    assert _wrapper_cache[key] is value
    del value
    gc.collect()
    assert reference() is None
    assert key not in _wrapper_cache


@pytest.mark.parametrize('factory', [DummyFactory.create_dummy_class, DummyFactory.create_dummy_interface])
def test_dropping_wrappers_releases_native_resources(factory):
    baseline = DummyFactory.get_native_live_count()
    destroyed = DummyFactory.get_native_destroyed_count()
    values = [factory() for _ in range(20)]
    references = [weakref.ref(value) for value in values]
    assert DummyFactory.get_native_live_count() == baseline + 20
    del values
    gc.collect()
    assert all(reference() is None for reference in references)
    assert DummyFactory.get_native_live_count() == baseline
    assert DummyFactory.get_native_destroyed_count() == destroyed + 20


@pytest.mark.parametrize('factory', [MultipleInheritanceFactory.get_multi_class,
                                     MultipleInheritanceFactory.get_multi_interface,
                                     MultipleInheritanceFactory.get_multi_class_as_narrow])
def test_derived_and_narrow_views_release_native_resources(factory):
    baseline = MultipleInheritanceFactory.get_native_live_count()
    destroyed = MultipleInheritanceFactory.get_native_destroyed_count()
    value = factory()
    reference = weakref.ref(value)
    assert MultipleInheritanceFactory.get_native_live_count() == baseline + 1
    del value
    gc.collect()
    assert reference() is None
    assert MultipleInheritanceFactory.get_native_live_count() == baseline
    assert MultipleInheritanceFactory.get_native_destroyed_count() == destroyed + 1


@pytest.mark.parametrize('get_child,get_parent', [
    (DummyFactory.get_dummy_child_class_singleton, DummyFactory.get_dummy_child_class_singleton_as_parent),
    (DummyFactory.get_dummy_child_interface_singleton, DummyFactory.get_dummy_child_interface_singleton_as_parent),
])
def test_live_wrapper_identity_and_native_retained_object_rewrap(get_child, get_parent):
    value = get_parent()
    assert get_child() is value
    reference = weakref.ref(value)
    identity = value._native.__gluecodium_id__()
    baseline = DummyFactory.get_native_live_count()
    del value
    gc.collect()
    assert reference() is None
    assert DummyFactory.get_native_live_count() == baseline
    replacement = get_child()
    assert replacement._native.__gluecodium_id__() == identity
    assert get_parent() is replacement
    assert reference() is None


def test_live_round_trips_preserve_identity():
    value = DummyFactory.create_dummy_class()
    assert DummyClass.dummy_class_round_trip(value) is value
    assert DummyClass.dummy_class_list_round_trip([value, value]) == [value, value]
    assert all(item is value for item in DummyClass.dummy_class_list_round_trip([value, value]))


def test_reused_native_address_does_not_return_a_stale_wrapper():
    baseline = DummyFactory.get_native_live_count()
    destroyed = DummyFactory.get_native_destroyed_count()
    old_references = []
    identity = None
    previous_generation = 0
    for _ in range(30):
        value = DummyFactory.create_reused_dummy_class()
        generation = DummyFactory.get_native_generation(value)
        assert generation > previous_generation
        previous_generation = generation
        current_identity = value._native.__gluecodium_id__()
        if identity is None:
            identity = current_identity
        assert current_identity == identity
        assert DummyClass.dummy_class_round_trip(value) is value
        old_references.append(weakref.ref(value))
        del value
        gc.collect()
        assert all(reference() is None for reference in old_references)
        assert (identity, None) not in _wrapper_cache
    assert DummyFactory.get_native_live_count() == baseline
    assert DummyFactory.get_native_destroyed_count() == destroyed + 30


def run_lifetime_case(code):
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stdout + result.stderr


def test_native_resource_release_and_shutdown_in_subprocess():
    run_lifetime_case('''
import atexit, gc, os, weakref
from test.DummyFactory import DummyFactory
from test.MultipleInheritanceFactory import MultipleInheritanceFactory
base = DummyFactory.get_native_live_count()
narrow_base = MultipleInheritanceFactory.get_native_live_count()
values = [DummyFactory.create_dummy_class(), DummyFactory.create_dummy_interface(),
          MultipleInheritanceFactory.get_multi_class_as_narrow()]
references = [weakref.ref(value) for value in values]
del values
gc.collect()
assert all(reference() is None for reference in references)
assert DummyFactory.get_native_live_count() == base
assert MultipleInheritanceFactory.get_native_live_count() == narrow_base
def check_shutdown():
    try:
        assert DummyFactory.get_native_live_count() == base
        assert MultipleInheritanceFactory.get_native_live_count() == narrow_base
    except BaseException:
        os._exit(1)
atexit.register(check_shutdown)
''')


def test_native_lambda_retains_python_callable_until_worker_cleanup():
    run_lifetime_case('''
import gc, threading, weakref
from test.ThreadedNotifier import ThreadedNotifier
notifier = ThreadedNotifier.create_on_new_thread()
started = threading.Event()
release = threading.Event()
seen = []
class Callback:
    def __call__(self, message):
        started.set()
        assert release.wait(10)
        seen.append(message)
callback = Callback()
reference = weakref.ref(callback)
notifier.notify_lambda_on_detached(callback, 'retained')
assert started.wait(10)
del callback
gc.collect()
assert reference() is not None
release.set()
notifier.wait_for_callbacks()
gc.collect()
assert seen == ['retained']
assert reference() is None
''')
