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

package com.here.gluecodium.generator.python

import com.here.gluecodium.generator.common.CommonGeneratorPredicates
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSignatureResolver
import com.here.gluecodium.model.lime.LimeStruct

/**
 * List of predicates used by `ifPredicate`/`unlessPredicate` template helpers in the Python generator.
 */
internal class PythonGeneratorPredicates(
    private val signatureResolver: LimeSignatureResolver,
    private val limeReferenceMap: Map<String, LimeElement>,
) {
    val predicates =
        mapOf(
            "hasAnyComment" to { limeElement: Any ->
                CommonGeneratorPredicates.hasAnyComment(limeElement, "Python")
            },
            "isInternal" to { it is LimeNamedElement && CommonGeneratorPredicates.isInternal(it, PYTHON) },
            "isPublic" to { it is LimeNamedElement && !CommonGeneratorPredicates.isInternal(it, PYTHON) },
            "isNestedInternal" to { limeElement: Any ->
                limeElement is LimeNamedElement &&
                    generateSequence(limeElement) {
                        limeReferenceMap[it.path.parent.toString()] as? LimeNamedElement
                    }.any { CommonGeneratorPredicates.isInternal(it, PYTHON) }
            },
            "isOverloaded" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    signatureResolver.isOverloaded(limeFunction)
            },
            "needsAllFieldsConstructor" to { limeStruct: Any ->
                when {
                    limeStruct !is LimeStruct -> false
                    limeStruct.fieldConstructors.isEmpty() -> true
                    limeStruct.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) ->
                        limeStruct.allFieldsConstructor == null
                    else -> false
                }
            },
        )
}
