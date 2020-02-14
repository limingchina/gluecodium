// -------------------------------------------------------------------------------------------------
// Copyright (C) 2016-2020 HERE Europe B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0
// License-Filename: LICENSE
//
// -------------------------------------------------------------------------------------------------

import "package:test/test.dart";
import "package:hello/hello.dart";
import "../test_suite.dart";

final _testSuite = TestSuite("Inheritance");

void main() {
  _testSuite.test("Create child class instance", () {
    final ChildClass result = ChildClass.createChildClass();

    expect(result.getName(), "Johnny");
    expect(result.luckyNumber, 7);

    result.release();
  });
  _testSuite.test("Cast child class instance to parent", () {
    final ParentInterface result = ChildClass.createChildClass();

    expect(result.getName(), "Johnny");
    expect(result.luckyNumber, 7);

    result.release();
  });
  _testSuite.test("Create grandchild class instance", () {
    final GrandchildClass result = GrandchildClass.createGrandchildClass();

    expect(result.getName(), "John F. Kimberly");
    expect(result.luckyNumber, 42);

    result.release();
  });
  _testSuite.test("Cast grandchild class instance to grandparent", () {
    final ParentInterface result = GrandchildClass.createGrandchildClass();

    expect(result.getName(), "John F. Kimberly");
    expect(result.luckyNumber, 42);

    result.release();
  });
  // TODO: #131 add tests for preserving type information
}
