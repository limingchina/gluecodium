# Copyright (C) 2026 HERE Europe B.V.
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

"""Syntax validation for the generated Python type stubs."""

import ast
from pathlib import Path

import functional


def test_generated_stubs_have_valid_syntax():
    module_dir = Path(functional.__file__).parent
    stub_files = [
        stub
        for package in ("test", "test_off", "another", "external")
        for stub in (module_dir / package).rglob("*.pyi")
    ]
    assert stub_files, "Generated type stubs must be present beside the extension"
    for stub in stub_files:
        ast.parse(stub.read_text(encoding="utf-8"), filename=str(stub))


def test_interface_stub_inheritance_preserves_bases_and_members(tmp_path):
    import os
    import subprocess
    import sys

    env = dict(os.environ, MYPYPATH=str(Path(functional.__file__).parent))
    command = [sys.executable, '-m', 'mypy', '--follow-imports=silent', '--show-error-codes',
               '--cache-dir', str(tmp_path / 'mypy-cache')]
    positive = tmp_path / 'inherited_interface_consumer.py'
    positive.write_text('''
from test.MultiInterface import MultiInterface
from test.RegularInterface import RegularInterface
from test.NarrowInterface import NarrowInterface

def consume(value: MultiInterface) -> None:
    regular: RegularInterface = value
    narrow: NarrowInterface = value
    value.parent_function()
    value.parent_property = "text"
    regular_text: str = value.parent_property
    narrow_text: str = value.parent_function_light()
    property_text: str = value.parent_property_light
    value.child_function()
    value.child_property = "child"
    child_text: str = value.child_property
''')
    result = subprocess.run(command + [str(positive)], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    negative = tmp_path / 'invalid_interface_consumer.py'
    negative.write_text('''
from test.MultiInterface import MultiInterface
from test.RegularInterface import RegularInterface
from test.MessageBox import MessageBox

def invalid(value: MultiInterface, unrelated: MessageBox) -> None:
    value.parent_property = 123
    regular: RegularInterface = unrelated
    value.missing_member()
''')
    result = subprocess.run(command + [str(negative)], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0
    assert result.stdout.count('[assignment]') == 2, result.stdout + result.stderr
    assert result.stdout.count('[attr-defined]') == 1, result.stdout + result.stderr
    assert 'Found 3 errors' in result.stdout, result.stdout + result.stderr


def test_struct_stub_constructor_signatures_match_public_native_calls(tmp_path):
    import os
    import subprocess
    import sys

    env = dict(os.environ, MYPYPATH=str(Path(functional.__file__).parent))
    command = [sys.executable, '-m', 'mypy', '--follow-imports=silent', '--show-error-codes',
               '--cache-dir', str(tmp_path / 'mypy-cache')]
    imports = '''
from test.ForecastData import ForecastData
from test.HiddenConstructorParameter import HiddenConstructorParameter
from test.FieldConstructorsAllDefaults import FieldConstructorsAllDefaults
from test.FieldConstructorsPartialDefaults import FieldConstructorsPartialDefaults
from test.ImmutableStructNoClash import ImmutableStructNoClash
from test.EquatableStructWithInternalFields import EquatableStructWithInternalFields
from test.SkipFieldInPlatformImmutable import SkipFieldInPlatformImmutable
from test.FieldCustomConstructorsMix import FieldCustomConstructorsMix
from test.OuterStructWithFieldConstructor import OuterStructWithFieldConstructor
from external.ExternalStruct import ExternalStruct
from external.AnotherExternalStruct import AnotherExternalStruct
'''
    positive = tmp_path / 'struct_constructor_consumer.py'
    positive.write_text(imports + '''
ForecastData()
ForecastData(-2, 26)
ForecastData(lowest_degree=-2, highest_degree=26)
FieldConstructorsAllDefaults()
FieldConstructorsAllDefaults(3)
FieldConstructorsAllDefaults(int_field=3, string_field="text")
FieldConstructorsAllDefaults(False, 3, "text")
FieldConstructorsPartialDefaults(3, "text")
FieldConstructorsPartialDefaults(bool_field=False, int_field=3, string_field="text")
ImmutableStructNoClash()
ImmutableStructNoClash(string_field="text", int_field=3, bool_field=True)
EquatableStructWithInternalFields(public_field="text")
SkipFieldInPlatformImmutable(int_field=3, bool_field=True)
FieldCustomConstructorsMix.create_me(int_value=3, dummy=1.0)
inner = OuterStructWithFieldConstructor.InnerStructWithDefaults()
OuterStructWithFieldConstructor(inner)
ExternalStruct()
ExternalStruct("plain", "accessor", [1, 2], AnotherExternalStruct(3))
ExternalStruct(string_field="plain", external_string_field="accessor", external_array_field=[1],
               external_struct_field=AnotherExternalStruct(int_field=3))
''')
    result = subprocess.run(command + [str(positive)], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    negative = tmp_path / 'invalid_constructor_consumer.py'
    negative.write_text(imports + '''
HiddenConstructorParameter()
ForecastData("wrong", 26)
ForecastData(unknown_field=1)
ForecastData(lowest_degree=1)
EquatableStructWithInternalFields(internal_field="hidden")
SkipFieldInPlatformImmutable(int_field=3, string_field="hidden", bool_field=True)
OuterStructWithFieldConstructor(42)
ExternalStruct("plain", "accessor", ["wrong"], AnotherExternalStruct(3))
''')
    result = subprocess.run(command + [str(negative)], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0
    assert result.stdout.count(' error: ') == 8, result.stdout + result.stderr
    assert 'Found 8 errors' in result.stdout, result.stdout + result.stderr
    assert '[name-defined]' not in result.stdout, result.stdout + result.stderr


def test_hidden_only_constructor_rejects_default_construction():
    import pytest
    from test.HiddenConstructorParameter import HiddenConstructorParameter

    with pytest.raises(TypeError):
        HiddenConstructorParameter()
