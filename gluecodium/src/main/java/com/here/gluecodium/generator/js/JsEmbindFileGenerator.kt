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

import com.here.gluecodium.generator.common.GeneratedFile
import com.here.gluecodium.generator.common.GenericIncludesCollector
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias

internal class JsEmbindFileGenerator(
    private val internalNamespace: List<String>,
    private val referenceMap: Map<String, LimeElement>,
    private val cppNameRules: CppNameRules,
    private val nameRules: JsNameRules,
    private val embindViewModelBuilder: JsEmbindViewModelBuilder,
    private val resolveRegisterName: (LimeNamedElement) -> String,
) {
    fun generate(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        filteredModel: LimeModel,
    ): List<GeneratedFile> {
        val limeType = limeElement as? LimeType ?: return emptyList()
        val allTypes = collectTypes(limeType)
        if (allTypes.isEmpty()) return emptyList()

        val includeResolver = EmbindIncludeResolver(referenceMap, cppNameRules, internalNamespace)
        val includeCollector = GenericIncludesCollector(includeResolver, retainPredicate = { true })
        val includes = allTypes.flatMap { includeCollector.collectImports(it) }.distinct().sorted()
        val bindings =
            allTypes.mapNotNull { type ->
                val templateName = selectTemplate(type) ?: return@mapNotNull null
                TemplateEngine.render(
                    templateName,
                    embindViewModelBuilder.build(type, filteredModel),
                    nameResolvers,
                )
            }
        val content =
            TemplateEngine.render(
                "js/EmbindFile",
                mapOf(
                    "includes" to includes,
                    "bindings" to bindings.joinToString("\n"),
                    "registerName" to resolveRegisterName(limeElement),
                ),
                nameResolvers,
            )
        return listOf(GeneratedFile(content, nameRules.getEmbindFileName(limeElement)))
    }

    fun collectTypes(limeType: LimeType): List<LimeType> {
        val result = mutableListOf<LimeType>()
        if (limeType !is LimeTypeAlias && limeType !is LimeLambda) {
            result.add(limeType)
        }
        val container = limeType as? LimeContainer ?: return result
        val nestedTypes =
            container.structs + container.classes + container.interfaces +
                container.enumerations + container.exceptions +
                container.typeAliases + container.lambdas
        for (nested in nestedTypes) {
            result.addAll(collectTypes(nested))
        }
        return result
    }

    private fun selectTemplate(limeElement: LimeNamedElement): String? =
        when (limeElement) {
            is LimeException -> "js/EmbindException"
            is LimeEnumeration -> "js/EmbindEnum"
            is LimeStruct -> "js/EmbindStruct"
            is LimeClass -> "js/EmbindClass"
            is LimeInterface -> "js/EmbindInterface"
            else -> null
        }
}