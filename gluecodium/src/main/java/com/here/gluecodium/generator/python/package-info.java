/*
 * Copyright (C) 2016-2025 HERE Europe B.V.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 * License-Filename: LICENSE
 */

/**
 * Python generator (pybind11 approach). Generates Python source files plus pybind11 C++
 * binding files that wrap the generated C++ API directly (no C-ABI intermediate layer).
 *
 * <p>The architecture mirrors the Swift generator: a platform-language generator
 * ({@code PythonGenerator}) plus a C++ binding generator ({@code Pybind11Generator}) that
 * both consume the same filtered LIME model.
 */
package com.here.gluecodium.generator.python;
