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

cmake_minimum_required(VERSION 3.10)
project(test_python)

if(NOT FUNCTIONAL_BUILD_PYTHON_TESTS)
  return()
endif()

find_program(PYTHON_EXE python3)
if(NOT PYTHON_EXE)
    message(FATAL_ERROR "Python 3 interpreter was not found")
endif()

# The extension module (functional_python) and the generated `test` wrapper package are built
# by the parent CMakeLists.txt and placed next to each other. Copy the test sources into the
# build directory and run pytest with both locations on the import path.
configure_file("pyproject.toml.in" "${CMAKE_CURRENT_BINARY_DIR}/pyproject.toml")
file(GLOB_RECURSE testFiles "test/*_test.py")
foreach(testFile ${testFiles})
    get_filename_component(testFileName ${testFile} NAME)
    configure_file(${testFile} "${CMAKE_CURRENT_BINARY_DIR}/tests/${testFileName}" COPYONLY)
endforeach()

# Run pytest with the build directory (which holds the .so and the `test` wrapper package) on
# the import path. The test files are copied into a `tests` subdirectory (not `test`) so that
# `import test` resolves to the generated wrapper package rather than the local test directory.
add_test(NAME unit_tests_python
    COMMAND ${PYTHON_EXE} -m pytest tests/ -v
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
set_tests_properties(unit_tests_python PROPERTIES
    ENVIRONMENT "PYTHONPATH=$<TARGET_FILE_DIR:functional_bindings_python>:${CMAKE_CURRENT_BINARY_DIR}")
