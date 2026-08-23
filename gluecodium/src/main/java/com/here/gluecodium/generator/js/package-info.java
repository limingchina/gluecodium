/*
 * Copyright (C) 2026 HERE Europe B.V.
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
 * JavaScript/WebAssembly generator (embind approach). Generates TypeScript declaration stubs plus
 * embind C++ binding files that wrap the generated C++ API directly (no C-ABI intermediate layer),
 * cross-compiled by `em++` into a `.wasm` binary.
 *
 * <p>The architecture mirrors {@code com.here.gluecodium.generator.python}: a platform-language
 * name resolver (JS/TS) paired with a C++-facing binding name resolver (embind).
 */
package com.here.gluecodium.generator.js;
