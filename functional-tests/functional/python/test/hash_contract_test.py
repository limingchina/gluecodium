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

"""Value hashes are reserved for immutable state and isolated key snapshots."""

import pytest
import functional
from test.Equatable import Equatable
from test.Maps import Maps
from test.SetType import SetType
from test.PointerEquatableClass import PointerEquatableClass
from test.EquatableClass import EquatableClass


@pytest.mark.parametrize('make', [
    Equatable.EquatableStruct,
    Equatable.EquatableNullableStruct,
    lambda: Equatable.ImmutableStruct(None, None, None, None, None,
        Equatable.NestedEquatableStruct('before'), None, None, None),
])
def test_reachable_mutable_structs_are_unhashable(make):
    value = make()
    with pytest.raises(TypeError):
        hash(value)
    with pytest.raises(TypeError):
        {value: 'saved'}


def test_deeply_immutable_structs_keep_value_hashes():
    left = Equatable.NestedImmutableStruct('same')
    right = Equatable.NestedImmutableStruct('same')
    assert left == right
    assert hash(left) == hash(right)
    assert {left: 'saved'}[right] == 'saved'


def test_snapshot_is_independent_and_equality_is_symmetric():
    value = Maps.EquatableStruct('original')
    key = value.as_key()
    assert value == key and key == value
    assert hash(key) == hash(value.as_key())
    mapping = {key: 'saved'}
    value.id = 'changed'
    assert mapping[key] == 'saved'
    assert key.id == 'original'
    assert key != value
    with pytest.raises(AttributeError):
        key.id = 'changed'
    with pytest.raises(AttributeError):
        key.__init__(value)
    key._native.id = 'detached native mutation'
    assert key.id == 'original'
    assert mapping[key] == 'saved'


def test_snapshot_nested_structs_and_collections_are_detached():
    value = Equatable.EquatableStruct()
    value.struct_field = Equatable.NestedEquatableStruct('original')
    value.array_field = ['original']
    value.map_field = {1: 'original'}
    key = value.as_key()
    mapping = {key: 'saved'}
    initial_hash = hash(key)
    value.struct_field.foo_field = 'original mutated'
    key.struct_field.foo_field = 'detached nested mutation'
    key.array_field.append('detached collection mutation')
    key.map_field[1] = 'detached map mutation'
    assert key.struct_field.foo_field == 'original'
    assert key.array_field == ['original']
    assert key.map_field == {1: 'original'}
    assert hash(key) == initial_hash
    assert mapping[key] == 'saved'


def test_struct_map_keys_cross_native_boundary_as_snapshots():
    key = Maps.EquatableStruct('key').as_key()
    result = Maps.struct_to_string_round_trip({key: 'saved'})
    returned = next(iter(result))
    assert result[key] == 'saved'
    assert returned == key
    with pytest.raises(AttributeError):
        returned.id = 'changed'
    returned._native.id = 'detached'
    assert result[key] == 'saved'


def test_struct_set_keys_cross_native_boundary_as_snapshots():
    key = SetType.EquatableStruct('key').as_key()
    result = SetType.struct_set_round_trip({key})
    returned = next(iter(result))
    assert key in result
    with pytest.raises(AttributeError):
        returned.id = 'changed'
    returned._native.id = 'detached'
    assert key in result


def test_native_transport_keys_use_stable_identity_equality_and_hashes():
    native_type = functional.test_Maps.EquatableStruct
    left = native_type('same')
    right = native_type('same')
    assert left != right
    original_hash = hash(left)
    mapping = {left: 'saved'}
    left.id = 'changed'
    assert hash(left) == original_hash
    assert mapping[left] == 'saved'
    assert left.__gluecodium_equals__(native_type('changed'))
    result = functional.test_Maps.struct_to_string_round_trip(mapping)
    assert list(result.values()) == ['saved']


def test_snapshot_rejects_reachable_value_equatable_class_references():
    value = PointerEquatableClass.EquatableStruct(
        EquatableClass.create('value'), PointerEquatableClass.create_new())
    with pytest.raises(TypeError, match='shared mutable'):
        value.as_key()


def test_snapshot_instance_methods_mutate_only_detached_copies():
    value = Maps.MutableHashState('original', Maps.EquatableStruct('nested'))
    key = value.as_key()
    mapping = {key: 'saved'}
    initial_hash = hash(key)
    key.mutate('detached method mutation')
    assert key.id == 'original'
    assert key.nested.id == 'nested'
    assert hash(key) == initial_hash
    assert mapping[key] == 'saved'
    value.mutate('original method mutation')
    assert value.id == 'original method mutation'
    assert mapping[key] == 'saved'


def test_default_casters_preserve_struct_field_and_nested_collection_keys():
    key = Maps.EquatableStruct('key').as_key()
    from test.SnapshotContainers import SnapshotContainers
    value = SnapshotContainers({key: 'saved'}, [{key}])
    assert value.keyed[key] == 'saved'
    assert key in value.grouped[0]
    returned = next(iter(value.keyed))
    with pytest.raises(AttributeError):
        returned.id = 'changed'
    returned._native.id = 'detached'
    assert value.keyed[key] == 'saved'


@pytest.mark.parametrize('kind', ['interface', 'lambda'])
def test_map_keys_cross_callback_boundaries_as_snapshots(kind):
    from test.HashMapCallback import HashMapCallback
    key = Maps.EquatableStruct('key').as_key()
    seen = []

    def round_trip(values):
        returned = next(iter(values))
        assert returned == key
        with pytest.raises(AttributeError):
            returned.id = 'changed'
        returned._native.id = 'detached'
        assert values[key] == 'saved'
        seen.append(returned)
        return values

    if kind == 'interface':
        class Listener(HashMapCallback):
            def round_trip(self, values):
                return round_trip(values)
        result = Maps.invoke_hash_callback(Listener(), {key: 'saved'})
    else:
        result = Maps.invoke_hash_lambda(round_trip, {key: 'saved'})
    assert result[key] == 'saved'
    assert len(seen) == 1


def test_snapshot_stub_preserves_struct_and_hashable_types(tmp_path):
    import os
    from pathlib import Path
    import subprocess
    import sys

    module_dir = Path(functional.__file__).parent
    positive = tmp_path / 'snapshot_consumer.py'
    positive.write_text("""
from typing import Hashable
from test.Equatable import Equatable
from test.Maps import Maps

def nested(value: Equatable.NestedEquatableStruct) -> None:
    key = value.as_key()
    ordinary: Equatable.NestedEquatableStruct = key
    hashable: Hashable = key
    field: str = key.foo_field

def top(value: Maps.EquatableStruct) -> None:
    key = value.as_key()
    ordinary: Maps.EquatableStruct = key
    hashable: Hashable = key
    field: str = key.id
""")
    env = dict(os.environ, MYPYPATH=str(module_dir))
    command = [sys.executable, '-m', 'mypy', '--follow-imports=silent', '--show-error-codes',
               '--cache-dir', str(tmp_path / 'mypy-cache')]
    result = subprocess.run(command + [str(positive)], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    negative = tmp_path / 'mutable_consumer.py'
    negative.write_text("""
from typing import Hashable
from test.Maps import Maps

def requires_hashable(value: Hashable) -> None: ...
def mutable(value: Maps.EquatableStruct) -> None:
    requires_hashable(value)
    wrong_field_type: int = value.as_key().id
""")
    result = subprocess.run(command + [str(negative)], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0
    assert result.stdout.count('[arg-type]') == 1, result.stdout + result.stderr
    assert result.stdout.count('[assignment]') == 1, result.stdout + result.stderr
    assert 'Found 2 errors' in result.stdout, result.stdout + result.stderr
