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
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeBasicType.TypeId

internal class JsCommonFileGenerator(
    private val internalNamespace: List<String>,
    private val referenceMap: Map<String, LimeElement>,
    private val cppNameRules: CppNameRules,
    private val embindNameResolver: EmbindNameResolver,
    private val requiresJsAdapter: (LimeTypeRef) -> Boolean,
    private val collectEmbindTypes: (LimeType) -> List<LimeType>,
    private val resolveRegisterName: (LimeNamedElement) -> String,
    private val nameRules: JsNameRules,
    private val jsModuleName: String,
    private val emitTypeScriptStubs: Boolean,
    private val isSupportedConstant: (LimeConstant) -> Boolean,
    private val isCppSkipped: (LimeNamedElement) -> Boolean,
    private val propertyAdapterName: (LimeProperty, String) -> String,
    private val overloadRuntimeName: (LimeFunction) -> String,
    private val structFunctionRuntimeName: (LimeFunction) -> String,
    private val overloadPredicate: (LimeFunction) -> String,
    private val instanceOverloadGroups: (LimeType, LimeModel) -> List<Map<String, Any>>,
) {
    fun generate(
        filteredModel: LimeModel,
        jsFilteredModel: LimeModel,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        val topLevelBoundTypes =
            filteredModel.topElements
                .filterIsInstance<LimeType>()
                .filter { it !is LimeTypeAlias && it !is LimeLambda }
        val boundTypes = topLevelBoundTypes.flatMap(collectEmbindTypes)
        val boundTypeNames = boundTypes.map(resolveRegisterName).toSet()
        val registerNameToDeps =
            boundTypes.associate { type ->
                val registerName = resolveRegisterName(type)
                val nestedTypeDeps =
                    if (type in topLevelBoundTypes) {
                        collectEmbindTypes(type).drop(1).map(resolveRegisterName)
                    } else {
                        emptyList()
                    }
                val parentDeps =
                    (type as? LimeContainerWithInheritance)?.parents
                        ?.mapNotNull { it.type.actualType }
                        ?.map(resolveRegisterName)
                        .orEmpty()
                registerName to (nestedTypeDeps + parentDeps)
                    .filter { it != registerName && it in boundTypeNames }
                    .distinct()
            }
        val genericRegistrations =
            JsGenericRegistrationCollector(
                referenceMap = referenceMap,
                cppNameRules = cppNameRules,
                internalNamespace = internalNamespace,
                embindNameResolver = embindNameResolver,
                requiresJsAdapter = requiresJsAdapter,
                collectEmbindTypes = collectEmbindTypes,
            ).collect(filteredModel)
        val moduleInitContent =
            TemplateEngine.render(
                "js/EmbindModuleInit",
                mapOf(
                    "moduleName" to jsModuleName,
                    "registerFunctions" to topologicalSort(registerNameToDeps).map { mapOf("name" to it) },
                    "genericRegistrations" to genericRegistrations.entries,
                    "genericRegistrationIncludes" to genericRegistrations.includes,
                    "needsUnorderedSet" to containsNullableSet(filteredModel),
                    "localeTypeName" to embindNameResolver.resolveName(TypeId.LOCALE),
                    "localeInclude" to (internalNamespace + "Locale.h").joinToString("/"),
                ),
                nameResolvers,
            )
        val wrapperTypeNames =
            filteredModel.topElements
                .filterIsInstance<LimeType>()
                .flatMap(collectEmbindTypes)
                .filter { it is LimeClass || it is LimeInterface }
                .map { nameRules.getEmbindRuntimeName(it) }
                .distinct()
        val wrapperTypes =
            wrapperTypeNames.mapIndexed { index, name ->
                mapOf("name" to name, "last" to (index == wrapperTypeNames.lastIndex))
            }
        val wrapperRuntimeContent =
            TemplateEngine.render(
                "js/JsWrapperRuntime",
                mapOf("wrapperTypes" to wrapperTypes),
                nameResolvers,
            )
        val moduleRuntimeContent =
            TemplateEngine.render(
                "js/JsModuleRuntime",
                mapOf("moduleFileName" to jsModuleName),
                nameResolvers,
            )
        val packageFiles =
            JsPackageGenerator(
                nameRules = nameRules,
                jsModuleName = jsModuleName,
                emitTypeScriptStubs = emitTypeScriptStubs,
                nameResolvers = nameResolvers,
                collectEmbindTypes = collectEmbindTypes,
                isSupportedConstant = isSupportedConstant,
                isCppSkipped = isCppSkipped,
                propertyAdapterName = propertyAdapterName,
                overloadRuntimeName = overloadRuntimeName,
                structFunctionRuntimeName = structFunctionRuntimeName,
                overloadPredicate = overloadPredicate,
                instanceOverloadGroups = instanceOverloadGroups,
            ).generate(jsFilteredModel)
        return packageFiles + listOf(
            GeneratedFile(moduleInitContent, JsNameRules.MODULE_INIT_FILE),
            GeneratedFile(wrapperRuntimeContent, JsNameRules.WRAPPER_RUNTIME_FILE),
            GeneratedFile(moduleRuntimeContent, JsNameRules.MODULE_RUNTIME_FILE),
        )
    }

    private fun containsNullableSet(filteredModel: LimeModel): Boolean {
        fun contains(typeRef: LimeTypeRef): Boolean {
            val type = typeRef.type
            if (typeRef.isNullable && type.actualType is LimeSet) return true
            return type.childTypes.any(::contains)
        }

        return filteredModel.topElements
            .filterIsInstance<LimeType>()
            .flatMap(collectEmbindTypes)
            .filterIsInstance<LimeContainer>()
            .any { container ->
                container.functions.any { function ->
                    function.parameters.any { contains(it.typeRef) } || contains(function.returnType.typeRef)
                } ||
                    container.properties.any { contains(it.typeRef) } ||
                    container.constants.any { contains(it.typeRef) } ||
                    container.constructors.any { constructor -> constructor.parameters.any { contains(it.typeRef) } } ||
                    (container as? LimeStruct)?.fields?.any { contains(it.typeRef) } == true
            }
    }

    private fun topologicalSort(parents: Map<String, List<String>>): List<String> {
        val visited = mutableSetOf<String>()
        val result = mutableListOf<String>()

        fun visit(name: String) {
            if (name in visited) return
            visited.add(name)
            parents[name].orEmpty().forEach(::visit)
            result.add(name)
        }
        parents.keys.sorted().forEach(::visit)
        return result
    }
}