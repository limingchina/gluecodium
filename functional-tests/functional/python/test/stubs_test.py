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
