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
project(greeter_python_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---------------------------------------------------------------------------
# Locate the Gluecodium CLI.
#
# The sample expects a built Gluecodium distribution. The easiest way is to
# run `./gradlew :gluecodium:installDist` in the Gluecodium repository root and
# point GLUECODIUM_BIN at the produced launcher:
#   <gluecodium-repo>/gluecodium/build/install/gluecodium/bin/gluecodium
#
# Alternatively set the GLUECODIUM_REPO environment variable to the repository
# root and this file derives the path automatically.
# ---------------------------------------------------------------------------
if(NOT GLUECODIUM_BIN)
  if(DEFINED ENV{GLUECODIUM_REPO})
    set(GLUECODIUM_BIN "$ENV{GLUECODIUM_REPO}/gluecodium/build/install/gluecodium/bin/gluecodium")
  else()
    set(GLUECODIUM_BIN "" CACHE FILEPATH "Path to the Gluecodium CLI binary")
  endif()
endif()

set(GLUECODIUM_EXECUTABLE "${GLUECODIUM_BIN}" CACHE FILEPATH "Gluecodium CLI")
if(NOT EXISTS "${GLUECODIUM_EXECUTABLE}")
  message(FATAL_ERROR
    "Gluecodium CLI not found at '${GLUECODIUM_EXECUTABLE}'. Build it with "
    "'./gradlew :gluecodium:installDist' and set -DGLUECODIUM_BIN=<path>, or set "
    "the GLUECODIUM_REPO env var to the repository root.")
endif()

# ---------------------------------------------------------------------------
# Generate C++ and Python (pybind11) sources from the LimeIDL file.
# ---------------------------------------------------------------------------
set(LIME_INPUT   "${CMAKE_CURRENT_SOURCE_DIR}/lime/Greeter.lime")
set(GEN_OUTPUT   "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(CPP_OUTPUT   "${GEN_OUTPUT}/cpp")
set(PY_OUTPUT    "${GEN_OUTPUT}/python")

# The name of the Python extension module (must match the PYBIND11_MODULE name).
# The C++ namespace is derived automatically from the Lime `package`
# (com.example.greeter), so we do not pass -cppnamespace here.
set(PY_MODULE    "greeter")

# Generate the C++ and Python (pybind11) sources from the LimeIDL file. This runs
# at *configure* time so the generated .cpp files exist before
# `python_add_library` is configured. Re-run CMake after editing Greeter.lime to
# regenerate.
message(STATUS "Generating bindings from ${LIME_INPUT}")
execute_process(
  COMMAND "${GLUECODIUM_EXECUTABLE}"
          -input  "${LIME_INPUT}"
          -output "${GEN_OUTPUT}"
          -generators cpp,python
          -pythonmodule "${PY_MODULE}"
  RESULT_VARIABLE _gluecodium_result
  OUTPUT_VARIABLE  _gluecodium_output
  ERROR_VARIABLE   _gluecodium_output)
if(NOT _gluecodium_result EQUAL 0)
  message(FATAL_ERROR "Gluecodium generation failed:\n${_gluecodium_output}")
endif()

# ---------------------------------------------------------------------------
# Build the CPython extension module.
#
# It links:
#   * the generated pybind11 register_* files (python/pybind11/*.cpp),
#   * the generated C++ headers + runtime (cpp/include, cpp/src),
#   * the hand-written implementation (cpp/GreeterImpl.cpp),
#   * the module entry point (cpp/module.cpp).
# ---------------------------------------------------------------------------
find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c "import pybind11; print(pybind11.get_include())"
  OUTPUT_VARIABLE PYBIND11_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)

# NOTE: the generated sources only exist after the `generate_bindings` custom
# command runs (at build time), so we list them explicitly rather than GLOB
# (a GLOB would evaluate at configure time and capture nothing).
set(PYBIND11_SOURCES
  "${PY_OUTPUT}/pybind11/com_example_greeter_Greeting.cpp"
  "${PY_OUTPUT}/pybind11/com_example_greeter_GreetingListener.cpp"
  "${PY_OUTPUT}/pybind11/com_example_greeter_Greeter.cpp"
  "${PY_OUTPUT}/pybind11/com_example_greeter_GreeterErrorCode.cpp"
  "${PY_OUTPUT}/pybind11/com_example_greeter_GreeterErrorError.cpp")
set(CPP_SOURCES
  "${CPP_OUTPUT}/src/LocaleImpl.cpp"
  "${CPP_OUTPUT}/src/TypeRepositoryImpl.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/Greeting.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/GreetingListener.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/Greeter.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/GreeterErrorCode.cpp")

python_add_library(greeter MODULE WITH_SOABI
  ${PYBIND11_SOURCES}
  ${CPP_SOURCES}
  "${CMAKE_CURRENT_SOURCE_DIR}/cpp/GreeterImpl.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/cpp/module.cpp")

target_include_directories(greeter PRIVATE
  "${PY_OUTPUT}"                       # generated python/ package (for _wrapper_cache.h etc.)
  "${CPP_OUTPUT}/include"              # generated C++ headers + runtime
  "${PYBIND11_INCLUDE_DIR}"
  "${Python_INCLUDE_DIRS}")

# The generated C++ uses an export macro; define it empty for a static build.
target_compile_definitions(greeter PRIVATE
  GLUECODIUM_CPP_EXPORT=
  GLUECODIUM_CPP_EXPORT_COMMON=)

# Copy the Python client next to the built module so `import greeter` resolves.
add_custom_command(TARGET greeter POST_BUILD
  COMMAND "${CMAKE_COMMAND}" -E copy
          "${CMAKE_CURRENT_SOURCE_DIR}/python/client.py"
          "$<TARGET_FILE_DIR:greeter>/client.py"
  COMMENT "Copying Python client next to the extension module")
