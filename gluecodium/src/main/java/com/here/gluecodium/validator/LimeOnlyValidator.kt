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

package com.here.gluecodium.validator

import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.generator.common.CommonGeneratorPredicates
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeType.DART
import com.here.gluecodium.model.lime.LimeAttributeType.JAVA
import com.here.gluecodium.model.lime.LimeAttributeType.KOTLIN
import com.here.gluecodium.model.lime.LimeAttributeType.ONLY
import com.here.gluecodium.model.lime.LimeAttributeType.SWIFT
import com.here.gluecodium.model.lime.LimeAttributeValueType
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeEnumerator
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeStruct

/**
 * Validates the correct usage of `@Only` attribute:
 * * `@Only` is mutually exclusive with `@Skip` and `@EnableIf`.
 * * `@Only` tags must be predefined language tags ("Java", "Kotlin", "Swift", "Dart", "Cpp").
 */
internal class LimeOnlyValidator(private val logger: LimeLogger) {
    fun validate(limeModel: LimeModel): Boolean {
        val allElements = limeModel.referenceMap.values.filterIsInstance<LimeNamedElement>()
        val validationResults = allElements.map { validateElement(it, limeModel.referenceMap) }

        return !validationResults.contains(false)
    }

    private fun validateElement(
        limeElement: LimeNamedElement,
        referenceMap: Map<String, LimeElement>,
    ): Boolean {
        val attributes = limeElement.attributes
        if (!attributes.have(ONLY)) return true

        // Check that @Only is not used on elements that can't be individually skipped
        when (limeElement) {
            is LimeEnumerator -> {
                logger.error(limeElement, "enumerator cannot be marked with an `@Only` attribute")
                return false
            }
            is LimeField -> {
                val parentStruct = referenceMap[limeElement.path.parent.toString()] as? LimeStruct
                if (parentStruct != null &&
                    CommonGeneratorPredicates.hasImmutableFields(parentStruct) &&
                    limeElement.defaultValue == null
                ) {
                    logger.error(
                        limeElement,
                        "field of an immutable struct without a default value cannot be marked with an `@Only` attribute",
                    )
                    return false
                }
            }
            else -> {}
        }

        // Check mutual exclusivity with @Skip
        if (attributes.have(LimeAttributeType.SKIP)) {
            logger.error(
                limeElement,
                "`@Only` attribute cannot be combined with `@Skip` attribute",
            )
            return false
        }

        // Check mutual exclusivity with @EnableIf
        if (attributes.have(LimeAttributeType.ENABLE_IF)) {
            logger.error(
                limeElement,
                "`@Only` attribute cannot be combined with `@EnableIf` attribute",
            )
            return false
        }

        // Check mutual exclusivity with per-platform @<Platform>(Skip) and @<Platform>(EnableIf)
        listOf(JAVA, KOTLIN, SWIFT, DART, CPP).forEach { platform ->
            if (attributes.have(platform, LimeAttributeValueType.SKIP)) {
                logger.error(
                    limeElement,
                    "`@Only` attribute cannot be combined with `@$platform(Skip)` attribute",
                )
                return false
            }
            if (attributes.have(platform, LimeAttributeValueType.ENABLE_IF)) {
                logger.error(
                    limeElement,
                    "`@Only` attribute cannot be combined with `@$platform(EnableIf)` attribute",
                )
                return false
            }
        }

        // Check that all @Only tags are predefined language tags
        val onlyTags = attributes.get(ONLY, LimeAttributeValueType.TAG, Any::class.java)
        val tagList =
            when (onlyTags) {
                is String -> listOf(onlyTags)
                is List<*> -> onlyTags.filterIsInstance<String>()
                else -> emptyList()
            }
        val validTags = setOf("Java", "Kotlin", "Swift", "Dart", "Cpp")
        val invalidTags = tagList.filterNot { tag -> validTags.any { it.equals(tag, ignoreCase = true) } }
        if (invalidTags.isNotEmpty()) {
            logger.error(
                limeElement,
                "`@Only` attribute only supports predefined language tags " +
                    "(Java, Kotlin, Swift, Dart, Cpp), but got: ${invalidTags.joinToString(", ")}",
            )
            return false
        }

        return true
    }
}
