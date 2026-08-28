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

package com.here.gluecodium.generator.js

import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeType

internal class JsOverloadGroupGenerator(
    private val nameRules: JsNameRules,
    private val inheritanceResolver: JsInheritanceResolver,
    private val overloadRuntimeName: (LimeFunction) -> String,
    private val overloadPredicate: (LimeFunction) -> String,
) {
    fun generate(type: LimeType, filteredModel: LimeModel): List<Map<String, Any>> {
        val container = type as? LimeContainer ?: return emptyList()
        val (secondaryFunctions, _) = inheritanceResolver.secondaryParentMembers(type, filteredModel)
        val functions =
            (inheritanceResolver.primaryInheritedOverloads(type, filteredModel) +
                container.functions.filterNot { it.isStatic || it.isConstructor } +
                secondaryFunctions)
                .distinctBy { it.fullName }
        return functions
            .groupBy { nameRules.getName(it) }
            .filterValues { overloads -> overloads.size > 1 }
            .map { (jsName, overloads) ->
                mapOf(
                    "jsName" to jsName,
                    "overloads" to overloads.map { function ->
                        mapOf(
                            "runtimeName" to overloadRuntimeName(function),
                            "predicate" to overloadPredicate(function),
                        )
                    },
                )
            }
    }
}