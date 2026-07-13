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
# Locate pybind11 + Python (needed both for the host C++ library and the
# extension module built by gluecodium_target_python_sources).
# ---------------------------------------------------------------------------
find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 REQUIRED)
set(PYBIND11_INCLUDE_DIR "${pybind11_INCLUDE_DIRS}")

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
# The Gluecodium CMake module (Phase 7) provides `gluecodium_target_python_sources`,
# which globs the generated pybind11 sources (python/pybind11/*.cpp — the per-type
# register_* functions AND the PYBIND11_MODULE entry point _module_init.cpp) and
# builds a `python_add_library(... MODULE WITH_SOABI)` extension module linked to the
# host C++ library.
#
# Generation runs at *configure* time (see above), so the generated .cpp files already
# exist when `gluecodium_target_python_sources` globs them. The helper exposes the
# module target as `greeter_python`, to which we add the hand-written implementation
# and the generated C++ runtime/impl sources.
# ---------------------------------------------------------------------------
if(DEFINED ENV{GLUECODIUM_REPO})
  set(_gluecodium_module_dir "$ENV{GLUECODIUM_REPO}/cmake/modules/gluecodium")
else()
  set(_gluecodium_module_dir "${CMAKE_CURRENT_SOURCE_DIR}/../../../cmake/modules/gluecodium")
endif()
include(${_gluecodium_module_dir}/Gluecodium.cmake)

# The host C++ library: generated abstract classes + runtime + hand-written impl.
add_library(greeter_cpp STATIC
  "${CPP_OUTPUT}/src/LocaleImpl.cpp"
  "${CPP_OUTPUT}/src/TypeRepositoryImpl.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/Greeting.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/GreetingListener.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/Greeter.cpp"
  "${CPP_OUTPUT}/src/com/example/greeter/GreeterErrorCode.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/cpp/GreeterImpl.cpp")
target_include_directories(greeter_cpp PRIVATE
  "${CPP_OUTPUT}/include"              # generated C++ headers + runtime
  "${PYBIND11_INCLUDE_DIR}")
target_compile_definitions(greeter_cpp PRIVATE
  GLUECODIUM_CPP_EXPORT=
  GLUECODIUM_CPP_EXPORT_COMMON=)

# Build the Python extension module from the generated pybind11 sources.
# Generation was done manually above (execute_process), so we pass OUTPUT_DIR explicitly
# (the directory that contains python/pybind11/*.cpp). When generation goes through
# gluecodium_generate instead, this argument can be omitted (it is read from the target's
# GLUECODIUM_OUTPUT_UNITY_DIR property, which also contains python/pybind11/).
gluecodium_target_python_sources(greeter_cpp
  MODULE_NAME "${PY_MODULE}"
  OUTPUT_DIR "${GEN_OUTPUT}"
  OUTPUT greeter_python)

# Copy the Python client next to the built module so `import greeter` resolves.
add_custom_command(TARGET ${greeter_python} POST_BUILD
  COMMAND "${CMAKE_COMMAND}" -E copy
          "${CMAKE_CURRENT_SOURCE_DIR}/python/client.py"
          "$<TARGET_FILE_DIR:${greeter_python}>/client.py"
  COMMENT "Copying Python client next to the extension module")
