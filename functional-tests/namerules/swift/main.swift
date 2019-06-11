// -------------------------------------------------------------------------------------------------
// Copyright (C) 2016-2019 HERE Europe B.V.
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

import XCTest
import namerules

class NameRulesTests: XCTestCase {
    func testAttributes() {
        let someClass = NameRules()
        someClass.isBooleanAttribute = true
        someClass.intAttribute = UInt32(8)
        someClass.structAttribute = NameRules.ExampleStruct(doubleValue: 3.14, intValues: [Int64(7)])
        XCTAssertTrue(someClass.isBooleanAttribute)
        XCTAssertEqual(someClass.intAttribute, UInt32(8))
        XCTAssertEqual(someClass.structAttribute.intValues, [Int64(7)])
    }

    func testError() {
        let someClass = NameRules()
        let someStruct = NameRules.ExampleStruct(doubleValue: 3.14, intValues: [Int64(7)])
        do {
            let _ = try someClass.someMethod(someArgument: someStruct)
            XCTFail("No exception was thrown")
        } catch NameRules.ExampleError.fatal {
        } catch {
            XCTFail("Wrong exception was thrown")
        }
    }

    static var allTests = [
        ("testAttributes", testAttributes),
        ("testError", testError)
    ]
}

let allTests = [
    testCase(NameRulesTests.allTests)
]

XCTMain(allTests)