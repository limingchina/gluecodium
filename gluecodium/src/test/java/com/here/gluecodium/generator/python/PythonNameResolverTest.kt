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

import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.generator.common.nameRuleSetFromConfig
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributes
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeBasicTypeRef
import com.here.gluecodium.model.lime.LimeDirectTypeRef
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimePath
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeValue
import com.natpryce.konfig.ConfigurationProperties
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith
import org.junit.runners.JUnit4
import java.util.logging.Logger

@RunWith(JUnit4::class)
class PythonNameResolverTest {
    private fun valueResolver() =
        PythonNameResolver(
            emptyMap(),
            PythonNameRules(nameRuleSetFromConfig(ConfigurationProperties.fromResource(javaClass, "/namerules/python.properties"))),
            LimeLogger(Logger.getAnonymousLogger(), emptyMap()),
            PythonCommentsProcessor(false),
        )

    @Test
    fun `renders nested collection keys as hashable Python values`() {
        val stringType = LimeBasicTypeRef(LimeBasicType.TypeId.STRING)
        val listType = LimeDirectTypeRef(LimeList(stringType))
        val setType = LimeDirectTypeRef(LimeSet(stringType))
        val value =
            LimeValue.InitializerList(
                LimeDirectTypeRef(LimeMap(listType, setType)),
                listOf(
                    LimeValue.KeyValuePair(
                        LimeValue.InitializerList(listType, listOf(LimeValue.Literal(stringType, "foo"))),
                        LimeValue.InitializerList(setType, listOf(LimeValue.Literal(stringType, "bar"))),
                    ),
                ),
            )
        assertEquals("{tuple([\"foo\"]): {\"bar\"}}", valueResolver().resolveName(value))
    }

    @Test
    fun `renders empty collections and nullable defaults`() {
        val stringType = LimeBasicTypeRef(LimeBasicType.TypeId.STRING)
        val resolver = valueResolver()
        assertEquals("set()", resolver.resolveName(LimeValue.InitializerList(LimeDirectTypeRef(LimeSet(stringType)), emptyList())))
        assertEquals("{}", resolver.resolveName(LimeValue.InitializerList(LimeDirectTypeRef(LimeMap(stringType, stringType)), emptyList())))
        assertEquals("None", resolver.resolveName(LimeValue.Null(stringType.asNullable())))
    }

    @Test
    fun `renders escaped square brackets without backslashes`() {
        val processor = PythonCommentsProcessor(false)

        assertEquals(
            "The range is [0, 23].",
            processor.process(
                "sdk.test.Type",
                "The range is \\[0, 23\\].",
                emptyMap(),
                null,
            ),
        )
    }

    @Test
    fun `resolves direct reference to retained duplicate type`() {
        val publicType = LimeStruct(LimePath(listOf("sdk", "routing"), listOf("TbtManeuver"), "public"))
        val internalType =
            LimeStruct(
                LimePath(listOf("sdk", "routing"), listOf("TbtManeuver"), "internal"),
                attributes =
                    LimeAttributes.Builder()
                        .addAttribute(LimeAttributeType.INTERNAL)
                        .build(),
            )
        val referenceMap = mapOf(internalType.path.toAmbiguousString() to internalType)
        val resolver =
            PythonNameResolver(
                referenceMap,
                PythonNameRules(
                    nameRuleSetFromConfig(
                        ConfigurationProperties.fromResource(javaClass, "/namerules/python.properties"),
                    ),
                ),
                LimeLogger(Logger.getAnonymousLogger(), emptyMap()),
                PythonCommentsProcessor(false),
            )

        assertEquals("_TbtManeuver", resolver.resolveName(LimeDirectTypeRef(publicType)))
    }
}
