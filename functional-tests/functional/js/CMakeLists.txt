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
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/load-package.mjs"
    "${JS_TEST_DIR}/load-package.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/strings.test.mjs"
    "${JS_TEST_DIR}/strings.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/builtin-types.test.mjs"
    "${JS_TEST_DIR}/builtin-types.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/enums.test.mjs"
    "${JS_TEST_DIR}/enums.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/structs.test.mjs"
    "${JS_TEST_DIR}/structs.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/blobs.test.mjs"
    "${JS_TEST_DIR}/blobs.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/classes.test.mjs"
    "${JS_TEST_DIR}/classes.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/locales.test.mjs"
    "${JS_TEST_DIR}/locales.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/immutable-structs.test.mjs"
    "${JS_TEST_DIR}/immutable-structs.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/interfaces.test.mjs"
    "${JS_TEST_DIR}/interfaces.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/listeners.test.mjs"
    "${JS_TEST_DIR}/listeners.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/listener-maps.test.mjs"
    "${JS_TEST_DIR}/listener-maps.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/complex-listeners.test.mjs"
    "${JS_TEST_DIR}/complex-listeners.test.mjs" COPYONLY)
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tests/listener-return-values.test.mjs"
    "${JS_TEST_DIR}/listener-return-values.test.mjs" COPYONLY)

add_test(NAME unit_tests_javascript
    COMMAND ${NODE_EXECUTABLE} --test
        "${JS_TEST_DIR}/strings.test.mjs"
        "${JS_TEST_DIR}/builtin-types.test.mjs"
        "${JS_TEST_DIR}/enums.test.mjs"
        "${JS_TEST_DIR}/structs.test.mjs"
        "${JS_TEST_DIR}/blobs.test.mjs"
        "${JS_TEST_DIR}/classes.test.mjs"
        "${JS_TEST_DIR}/locales.test.mjs"
        "${JS_TEST_DIR}/immutable-structs.test.mjs"
        "${JS_TEST_DIR}/interfaces.test.mjs"
        "${JS_TEST_DIR}/listeners.test.mjs"
        "${JS_TEST_DIR}/listener-maps.test.mjs"
        "${JS_TEST_DIR}/complex-listeners.test.mjs"
        "${JS_TEST_DIR}/listener-return-values.test.mjs")
set_tests_properties(unit_tests_javascript PROPERTIES
    ENVIRONMENT "GLUECODIUM_JS_MODULE=$<TARGET_FILE:functional_bindings_js>")