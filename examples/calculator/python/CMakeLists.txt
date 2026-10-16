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

cmake_minimum_required(VERSION 3.19)
project(calculator_python_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# The static C++ library will be linked into a shared Python extension.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 3.10 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

set(GLUECODIUM_BIN "" CACHE FILEPATH "Path to the built Gluecodium CLI")
if(NOT EXISTS "${GLUECODIUM_BIN}")
  message(FATAL_ERROR
    "Build Gluecodium with './gradlew :gluecodium:installDist', then set "
    "-DGLUECODIUM_BIN=<repo>/gluecodium/build/install/gluecodium/bin/gluecodium")
endif()

set(GEN_OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(CPP_OUTPUT "${GEN_OUTPUT}/cpp")
set(PY_OUTPUT "${GEN_OUTPUT}/python")
set(PY_MODULE "calculator")

# Generate at configure time so pybind11's source list exists before creating
# the extension target. Reconfigure after editing LimeIDL or the generator.
execute_process(
  COMMAND "${GLUECODIUM_BIN}"
          -input "${CMAKE_CURRENT_SOURCE_DIR}/../lime/Calculator.lime"
          -output "${GEN_OUTPUT}"
          -generators cpp,python
          -pythonmodule "${PY_MODULE}"
          -intnamespace gluecodium
  RESULT_VARIABLE generation_result
  OUTPUT_VARIABLE generation_stdout
  ERROR_VARIABLE generation_stderr)
if(NOT generation_result EQUAL 0)
  message(FATAL_ERROR "Gluecodium generation failed:\n${generation_stdout}\n${generation_stderr}")
endif()

include("${CMAKE_CURRENT_SOURCE_DIR}/../../../cmake/modules/gluecodium/Gluecodium.cmake")

add_library(calculator_cpp STATIC
  "${CPP_OUTPUT}/src/gluecodium/LocaleImpl.cpp"
  "${CPP_OUTPUT}/src/gluecodium/TypeRepositoryImpl.cpp"
  "${CPP_OUTPUT}/src/gluecodium/StringViewImplDefs.cpp"
  "${CPP_OUTPUT}/src/gluecodium/calculator/Calculator.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/../cpp/CalculatorImpl.cpp")
target_include_directories(calculator_cpp PUBLIC "${CPP_OUTPUT}/include")
# This example links the API statically; it does not export a separate library.
target_compile_definitions(calculator_cpp PUBLIC
  GLUECODIUM_CPP_EXPORT=
  GLUECODIUM_CPP_EXPORT_COMMON=)

gluecodium_target_python_sources(calculator_cpp
  MODULE_NAME "${PY_MODULE}"
  OUTPUT_DIR "${GEN_OUTPUT}"
  OUTPUT calculator_extension)

# Keep the native extension, wrapper import root, and client together.
add_custom_target(calculator_python_files ALL
  COMMAND "${CMAKE_COMMAND}" -E copy
          "${CMAKE_CURRENT_SOURCE_DIR}/client.py"
          "$<TARGET_FILE_DIR:${calculator_extension}>/client.py"
  COMMAND "${CMAKE_COMMAND}" -E copy_directory
          "${PY_OUTPUT}/gluecodium"
          "$<TARGET_FILE_DIR:${calculator_extension}>/gluecodium"
  COMMAND "${CMAKE_COMMAND}" -E copy
          "${PY_OUTPUT}/__init__.py"
          "${PY_OUTPUT}/_native_base.py"
          "$<TARGET_FILE_DIR:${calculator_extension}>/"
  DEPENDS ${calculator_extension}
  COMMENT "Copying the generated Python wrappers and calculator client")

# Run with the exact interpreter selected for the extension build.
enable_testing()
add_test(NAME calculator_client
  COMMAND "${Python3_EXECUTABLE}" "$<TARGET_FILE_DIR:${calculator_extension}>/client.py")
