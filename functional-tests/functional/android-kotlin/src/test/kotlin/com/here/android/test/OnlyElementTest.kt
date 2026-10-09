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
package com.here.android.test

import com.here.android.RobolectricApplication
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(application = RobolectricApplication::class)
class OnlyElementTest {
    @Test
    fun selectedMethodsRoundTrip() {
        val input = "Only: Kotlin round trip"
        // The shared method also works when Java-generated JNI is enforced.
        assertEquals(input, OnlyFunctions.shared(input))
        assertEquals(22, OnlyFunctions.KOTLIN_CONSTANT)
    }

    @Test
    fun otherPlatformsAreExcluded() {
        assertNotNull(OnlyFunctions.Companion::class.java.getDeclaredMethod("kotlinOnly", String::class.java))
        val excludedMethods = setOf("javaOnly", "swiftOnly", "dartOnly", "cppOnly")
        val excludedConstants = setOf("JAVA_CONSTANT", "SWIFT_CONSTANT", "DART_CONSTANT", "CPP_CONSTANT")
        for (method in OnlyFunctions.Companion::class.java.declaredMethods) {
            assertFalse(method.name in excludedMethods)
        }
        for (field in OnlyFunctions::class.java.declaredFields) {
            assertFalse(field.name in excludedConstants)
        }
    }
}
