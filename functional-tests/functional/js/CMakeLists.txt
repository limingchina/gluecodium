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

cmake_minimum_required(VERSION 3.20)
project(test_javascript)

if(NOT FUNCTIONAL_BUILD_JS_TESTS)
    return()
endif()

find_program(NODE_EXECUTABLE node REQUIRED)

set(JS_TEST_DIR "${CMAKE_CURRENT_BINARY_DIR}/tests")
file(MAKE_DIRECTORY "${JS_TEST_DIR}")
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/strings.test.mjs"
    "${JS_TEST_DIR}/strings.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/builtin-types.test.mjs"
    "${JS_TEST_DIR}/builtin-types.test.mjs" COPYONLY)

add_test(NAME unit_tests_javascript
    COMMAND ${NODE_EXECUTABLE} --test
        "${JS_TEST_DIR}/strings.test.mjs"
        "${JS_TEST_DIR}/builtin-types.test.mjs")
set_tests_properties(unit_tests_javascript PROPERTIES
    ENVIRONMENT "GLUECODIUM_JS_MODULE=$<TARGET_FILE:functional_bindings_js>")