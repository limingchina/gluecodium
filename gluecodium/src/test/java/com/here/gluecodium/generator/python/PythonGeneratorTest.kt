/*
 * Copyright (C) 2016-2026 HERE Europe B.V.
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

package com.here.gluecodium.generator.python

import com.here.gluecodium.generator.common.GeneratorOptions
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimePath
import com.here.gluecodium.model.lime.LimeStruct
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PythonGeneratorTest {
    @Test
    fun `canonical wrappers use configured external Python imports`() {
        val type =
            LimeClass(
                LimePath(listOf("test"), listOf("External")),
                external =
                    LimeExternalDescriptor.Builder()
                        .addValue("cpp", "name", "external::External")
                        .addValue("cpp", "include", "External.h")
                        .addValue("python", "importPath", "client.external")
                        .build(),
            )
        val model = LimeModel(mapOf(type.path.toString() to type), listOf(type))
        val generator = PythonGenerator().apply { initialize(GeneratorOptions()) }
        val runtime = generator.generate(model).single { it.targetFile.path == "python/_native_base.py" }.content

        assertTrue(runtime.contains("\"test_External\", \"client.external\", \"External\", False"))
    }

    @Test
    fun `opaque declarations are independent of reference map order`() {
        val structs =
            listOf("Alpha", "Beta").map { name ->
                LimeStruct(
                    LimePath(listOf("test"), listOf(name)),
                    external =
                        LimeExternalDescriptor.Builder()
                            .addValue("cpp", "name", "external::$name")
                            .addValue("cpp", "include", "External.h")
                            .build(),
                )
            }

        fun generateHeader(types: List<LimeStruct>): String {
            val model = LimeModel(types.associateBy { it.path.toString() }, structs)
            val generator = PythonGenerator().apply { initialize(GeneratorOptions()) }
            return generator.generate(model).single {
                it.targetFile.path == "python/pybind11/_opaque_types.h"
            }.content
        }

        assertEquals(generateHeader(structs), generateHeader(structs.reversed()))
    }
}
