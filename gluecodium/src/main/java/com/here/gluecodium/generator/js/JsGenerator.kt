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

import com.here.gluecodium.cli.GluecodiumExecutionException
import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.common.LimeModelFilter
import com.here.gluecodium.common.LimeModelSkipPredicates
import com.here.gluecodium.generator.common.GeneratedFile
import com.here.gluecodium.generator.common.Generator
import com.here.gluecodium.generator.common.GeneratorOptions
import com.here.gluecodium.generator.common.GenericImportsCollector
import com.here.gluecodium.generator.common.GenericIncludesCollector
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.nameRuleSetFromConfig
import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.generator.cpp.CppSignatureResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.SKIP
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import java.util.logging.Logger

/**
 * Generates JavaScript/TypeScript bindings on top of the C++ API using Emscripten embind.
 *
 * <p>Architecturally this mirrors the Python generator: it produces TypeScript declaration stubs
 * (`.d.ts`) plus embind C++ binding files that `#include` the generated C++ headers and register
 * the C++ API via `EMSCRIPTEN_BINDINGS` blocks (no intermediate C-ABI shim). The entire output is
 * cross-compiled by `em++` into a single `.wasm` binary plus a JS glue/loader file.
 */
internal class JsGenerator : Generator {
    private lateinit var internalNamespace: List<String>
    private lateinit var rootNamespace: List<String>
    private lateinit var commentsProcessor: JsCommentsProcessor
    private lateinit var cppNameRules: CppNameRules
    private lateinit var nameRules: JsNameRules
    private lateinit var jsModuleName: String
    private lateinit var activeTags: Set<String>

    private lateinit var limeReferenceMap: Map<String, LimeElement>
    private lateinit var jsNameResolver: JsNameResolver
    private lateinit var embindNameResolver: EmbindNameResolver
    private lateinit var cppNameCache: CppNameCache

    override val shortName = "js"

    override fun initialize(options: GeneratorOptions) {
        internalNamespace = options.cppInternalNamespace
        rootNamespace = options.cppRootNamespace
        commentsProcessor = JsCommentsProcessor(options.werror.contains(GeneratorOptions.WARNING_DOC_LINKS))
        cppNameRules = CppNameRules(rootNamespace, nameRuleSetFromConfig(options.cppNameRules))
        nameRules = JsNameRules(nameRuleSetFromConfig(options.jsNameRules))
        jsModuleName = options.jsModuleName
        activeTags = options.tags
    }

    override fun generate(limeModel: LimeModel): List<GeneratedFile> {
        val limeLogger = LimeLogger(logger, limeModel.fileNameMap)

        // Filter the model for the embind C++ binding output: retain functions/fields (needed
        // for binding bodies). External types are NOT skipped — embind still needs to `#include`
        // and bind external C++ types referenced by other bound types.
        val embindFilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, JS, retainFunctionsAndFields = true) &&
                    !isCppSkipped(it)
            }
        // Filter the model for the TypeScript `.d.ts` stub output.
        val jsFilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, JS, retainFunctionsAndFields = false)
            }

        jsNameResolver = JsNameResolver(embindFilteredModel.referenceMap, nameRules, limeLogger, commentsProcessor)

        limeReferenceMap = embindFilteredModel.referenceMap

        cppNameCache = CppNameCache(rootNamespace, embindFilteredModel.referenceMap, cppNameRules)
        embindNameResolver =
            EmbindNameResolver(
                embindFilteredModel.referenceMap,
                internalNamespace,
                cppNameCache,
                cppNameRules,
            )

        val nameResolvers =
            mapOf(
                "" to jsNameResolver,
                "Embind" to embindNameResolver,
                "C++" to embindNameResolver,
            )

        val importsCollector =
            GenericImportsCollector(
                JsImportResolver(limeReferenceMap, nameRules),
                collectTypeRefImports = true,
                collectValueImports = false,
                parentTypeFilter = { true },
                collectTypeAliasImports = true,
            )

        val stubFiles =
            jsFilteredModel.topElements.flatMap { generateStubFile(it, importsCollector, nameResolvers) }
        val embindFiles =
            embindFilteredModel.topElements.flatMap {
                generateEmbindFile(it, nameResolvers, embindFilteredModel)
            }

        if (commentsProcessor.hasError) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        return stubFiles + embindFiles +
            generateCommonFiles(embindFilteredModel, nameResolvers)
    }

    private fun generateStubFile(
        limeElement: LimeNamedElement,
        importsCollector: GenericImportsCollector<JsImport>,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        val templateName = selectStubTemplate(limeElement) ?: return emptyList()
        val selfModulePath = "./" + (limeElement.path.head + nameRules.getName(limeElement)).joinToString("/")
        val imports =
            importsCollector.collectImports(limeElement)
                .filterNot { it.modulePath == selfModulePath }
                .distinct()
                .sorted()

        val content =
            TemplateEngine.render(
                templateName,
                mapOf(
                    "model" to limeElement,
                    "imports" to imports,
                    "moduleName" to jsModuleName,
                ) + stubViewModel(limeElement),
                nameResolvers,
            )
        return listOf(GeneratedFile(content, nameRules.getJsStubFileName(limeElement)))
    }

    private fun stubViewModel(limeElement: LimeNamedElement): Map<String, Any> {
        val data = mutableMapOf<String, Any>(
            "jsName" to nameRules.getName(limeElement),
        )
        val container = limeElement as? com.here.gluecodium.model.lime.LimeContainer
        if (container != null) {
            data["constructors"] = container.constructors.map { functionStubViewModel(it) }
            data["functions"] = container.functions.map { functionStubViewModel(it) }
            data["properties"] = container.properties.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "jsType" to jsNameResolver.resolveName(it.typeRef),
                    "isStatic" to it.isStatic,
                )
            }
        }
        if (limeElement is LimeStruct) {
            data["fields"] = limeElement.fields.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "jsType" to jsNameResolver.resolveName(it.typeRef),
                )
            }
        }
        if (limeElement is com.here.gluecodium.model.lime.LimeEnumeration) {
            data["enumerators"] = limeElement.enumerators.map { mapOf("jsName" to nameRules.getName(it)) }
        }
        return data
    }

    private fun functionStubViewModel(function: LimeFunction): Map<String, Any> =
        mapOf(
            "jsName" to nameRules.getName(function),
            "isConstructor" to function.isConstructor,
            "isStatic" to function.isStatic,
            "returnType" to jsNameResolver.resolveName(function.returnType),
            "parameters" to function.parameters.mapIndexed { index, parameter ->
                mapOf(
                    "jsName" to nameRules.getName(parameter),
                    "jsType" to jsNameResolver.resolveName(parameter.typeRef),
                    "last" to (index == function.parameters.lastIndex),
                )
            },
        )

    private fun generateEmbindFile(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        filteredModel: LimeModel,
    ): List<GeneratedFile> {
        val limeType = limeElement as? com.here.gluecodium.model.lime.LimeType ?: return emptyList()
        val allTypes = collectEmbindTypes(limeType)
        if (allTypes.isEmpty()) return emptyList()

        val includeResolver = EmbindIncludeResolver(limeReferenceMap, cppNameRules, internalNamespace)
        val includeCollector = GenericIncludesCollector(includeResolver, retainPredicate = { true })
        val includes =
            allTypes.flatMap { includeCollector.collectImports(it) }.distinct().sorted()

        val bindings =
            allTypes.mapNotNull { type ->
                val templateName = selectEmbindTemplate(type) ?: return@mapNotNull null
                TemplateEngine.render(
                    templateName,
                    buildEmbindViewModel(type, filteredModel),
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

    /** Prefers an `open class` parent over a narrow interface as the single embind `base<>`. */
    private fun primaryBaseOf(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): String? =
        primaryBaseType(type, filteredModel)
            ?.let { cppNameCache.getFullyQualifiedName(it) }

    private fun primaryBaseType(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): LimeContainerWithInheritance? =
        (type as? LimeContainerWithInheritance)?.parents
            ?.mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
            ?.filter { filteredModel.referenceMap.containsKey(it.fullName) }
            ?.minByOrNull { it is com.here.gluecodium.model.lime.LimeInterface }

    private fun secondaryParentMembers(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): Pair<List<LimeFunction>, List<LimeProperty>> {
        val container = type as? LimeContainerWithInheritance ?: return emptyList<LimeFunction>() to emptyList()
        val primaryBase = primaryBaseType(type, filteredModel)
        val secondaryParents =
            container.parents
                .mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
                .filter { it !== primaryBase && filteredModel.referenceMap.containsKey(it.fullName) }
        val functions =
            secondaryParents
                .flatMap { it.functions + it.inheritedFunctions }
                .distinctBy { it.fullName }
        val properties =
            secondaryParents
                .flatMap { it.properties + it.inheritedProperties }
                .distinctBy { it.fullName }
        return functions to properties
    }

    /**
     * Builds the template data for one embind binding: the common identity fields plus
     * member view models (constructors, functions, properties, fields, enumerators,
     * constants) resolved against both the C++ names (for the binding body) and the JS
     * names (for the registered identifiers).
     */
    private fun buildEmbindViewModel(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): Map<String, Any> {
        val data = mutableMapOf<String, Any>(
            "model" to type,
            "internalNamespace" to internalNamespace,
            "jsName" to nameRules.getName(type),
            "cppFullName" to cppNameCache.getFullyQualifiedName(type),
            "registerName" to resolveRegisterName(type),
        )
        primaryBaseOf(type, filteredModel)?.let { data["primaryBase"] = it }
        if (type is com.here.gluecodium.model.lime.LimeEnumeration) {
            val enumerators = type.enumerators.map { enumeratorViewModel(it) }
            data["enumeratorBindings"] = enumerators.joinToString("\n") {
                "    .value(\"${it["jsName"]}\", ${it["cppName"]})"
            }
        }
        val container = type as? com.here.gluecodium.model.lime.LimeContainer ?: return data

        val (secondaryFunctions, secondaryProperties) = secondaryParentMembers(type, filteredModel)
        data["constructors"] = container.constructors.map { functionViewModel(it) }
        data["methods"] =
            (container.functions.filterNot { it.isConstructor } + secondaryFunctions)
                .distinctBy { it.fullName }
                .map {
                    functionViewModel(
                        it,
                        isFlattened = secondaryFunctions.contains(it),
                        flattenedReceiverType = cppNameCache.getFullyQualifiedName(type),
                    )
                }
        data["properties"] =
            (container.properties + secondaryProperties)
                .distinctBy { it.fullName }
                .map { propertyViewModel(it) }
        if (type is LimeStruct) {
            data["fields"] = type.fields.map { fieldViewModel(type, it) }
        }
        data["constants"] = container.constants.map { constantViewModel(it) }
        return data
    }

    private fun functionViewModel(
        function: LimeFunction,
        isFlattened: Boolean = false,
        flattenedReceiverType: String? = null,
    ): Map<String, Any> {
        val isOverloaded = CppSignatureResolver(limeReferenceMap, cppNameRules).isOverloaded(function)
        val returnType = function.returnType.typeRef
        val returnActualType = returnType.type.actualType
        val needsAdapter =
            returnType.isNullable || returnActualType is LimeList || returnActualType is LimeMap ||
                function.parameters.any { parameter ->
                    parameter.typeRef.isNullable ||
                        parameter.typeRef.type.actualType is LimeList ||
                        parameter.typeRef.type.actualType is LimeMap
                }
        return mapOf(
            "model" to function,
            "jsName" to nameRules.getName(function),
            "cppName" to embindNameResolver.resolveName(function),
            "isConstructor" to function.isConstructor,
            "isStatic" to function.isStatic,
            "needsAdapter" to needsAdapter,
            "adapterReturnType" to
                if (returnType.isNullable || returnActualType is LimeList || returnActualType is LimeMap) {
                    "emscripten::val"
                } else {
                    embindNameResolver.resolveName(returnType)
                },
            "returnIsNullable" to returnType.isNullable,
            "returnIsList" to (returnActualType is LimeList),
            "returnIsMap" to (returnActualType is LimeMap),
            // Overloads are registered with explicit signatures via select_overload.
            "isOverloaded" to isOverloaded,
            "isFlattened" to isFlattened,
            "parameters" to function.parameters.mapIndexed { index, parameter ->
                val actualType = parameter.typeRef.type.actualType
                mapOf(
                    "model" to parameter,
                    "jsName" to nameRules.getName(parameter),
                    "cppType" to embindNameResolver.resolveName(parameter.typeRef),
                    "adapterType" to
                        if (parameter.typeRef.isNullable || actualType is LimeList || actualType is LimeMap) {
                            "emscripten::val"
                        } else {
                            embindNameResolver.resolveName(parameter.typeRef)
                        },
                    "nativeName" to parameter.path.name,
                    "nativeType" to embindNameResolver.resolveName(parameter.typeRef),
                    "underlyingType" to embindNameResolver.resolveName(parameter.typeRef.type),
                    "isNullable" to parameter.typeRef.isNullable,
                    "isList" to (actualType is LimeList),
                    "isMap" to (actualType is LimeMap),
                    "mapKeyType" to (actualType as? LimeMap)?.let { embindNameResolver.resolveName(it.keyType) },
                    "mapValueType" to (actualType as? LimeMap)?.let { embindNameResolver.resolveName(it.valueType) },
                    "last" to (index == function.parameters.lastIndex),
                )
            },
        ).toMutableMap().apply {
            val parameters = function.parameters.mapIndexed { index, parameter ->
                val actualType = parameter.typeRef.type.actualType
                val nativeType = embindNameResolver.resolveName(parameter.typeRef)
                val adapterType =
                    if (parameter.typeRef.isNullable || actualType is LimeList || actualType is LimeMap) {
                        "emscripten::val"
                    } else {
                        nativeType
                    }
                val callName = if (parameter.typeRef.isNullable || actualType is LimeList || actualType is LimeMap) {
                    "${parameter.path.name}_value"
                } else {
                    parameter.path.name
                }
                mapOf(
                    "type" to adapterType,
                    "name" to parameter.path.name,
                    "last" to (index == function.parameters.lastIndex),
                    "callName" to callName,
                    "preparation" to adapterParameterPreparation(parameter, callName),
                )
            }
            put("adapterParameters", parameters.joinToString(", ") { "${it["type"]} ${it["name"]}" })
            put("adapterSignatureParameters", parameters.joinToString(", ") { it["type"].toString() })
            put("adapterCallArguments", parameters.joinToString(", ") { it["callName"].toString() })
            put("adapterPreparations", parameters.map { it["preparation"] }.filter { it is String && it.isNotEmpty() }.joinToString("\n"))
            put(
                "adapterCallPrefix",
                if (returnType.isNullable || returnActualType is LimeList || returnActualType is LimeMap) {
                    "auto result = "
                } else {
                    "return "
                },
            )
            put("adapterReturnConversion", adapterReturnConversion(returnType, returnActualType))
            if (isFlattened) {
                val receiverType = flattenedReceiverType ?: error("Missing flattened receiver type")
                put(
                    "flattenedFunctionSignature",
                    listOf(
                        "${if (returnType.isNullable || returnActualType is LimeList || returnActualType is LimeMap) "emscripten::val" else embindNameResolver.resolveName(returnType)}($receiverType*",
                        *parameters.map { it["type"].toString() }.toTypedArray(),
                    )
                        .joinToString(", ")
                        .let { "$it)" },
                )
                put(
                    "flattenedLambdaParameters",
                    listOf("$receiverType* self", *parameters.map { "${it["type"]} ${it["name"]}" }.toTypedArray())
                        .joinToString(", "),
                )
            }
        }
    }

    private fun adapterParameterPreparation(parameter: com.here.gluecodium.model.lime.LimeParameter, callName: String): String {
        val typeRef = parameter.typeRef
        val actualType = typeRef.type.actualType
        val nativeType = embindNameResolver.resolveName(typeRef)
        return when {
            typeRef.isNullable ->
                "auto $callName = ${parameter.path.name}.isNull() || ${parameter.path.name}.isUndefined() ? $nativeType{} : $nativeType(${parameter.path.name}.as<${embindNameResolver.resolveName(typeRef.type)}>());"
            actualType is LimeList -> {
                val elementType = embindNameResolver.resolveName(actualType.elementType)
                "auto $callName = emscripten::vecFromJSArray<$elementType>(${parameter.path.name});"
            }
            actualType is LimeMap -> {
                val keyType = embindNameResolver.resolveName(actualType.keyType)
                val valueType = embindNameResolver.resolveName(actualType.valueType)
                "${nativeType} $callName; for (const auto& entry : ${parameter.path.name}.call<emscripten::val>(\"entries\")) { $callName.emplace(entry[0].as<$keyType>(), entry[1].as<$valueType>()); }"
            }
            else -> ""
        }
    }

    private fun adapterReturnConversion(
        returnType: com.here.gluecodium.model.lime.LimeTypeRef,
        actualType: com.here.gluecodium.model.lime.LimeType,
    ): String {
        val source = if (returnType.isNullable) "*result" else "result"
        return when {
            returnType.isNullable && actualType is LimeMap ->
                "if (!result) return emscripten::val::undefined(); auto jsResult = emscripten::val::global(\"Map\").new_(); for (const auto& entry : $source) { jsResult.call<void>(\"set\", emscripten::val(entry.first), emscripten::val(entry.second)); } return jsResult;"
            actualType is LimeMap ->
                "auto jsResult = emscripten::val::global(\"Map\").new_(); for (const auto& entry : $source) { jsResult.call<void>(\"set\", emscripten::val(entry.first), emscripten::val(entry.second)); } return jsResult;"
            returnType.isNullable ->
                "return result ? emscripten::val($source) : emscripten::val::undefined();"
            actualType is LimeList ->
                "return emscripten::val::array($source.begin(), $source.end());"
            else -> ""
        }
    }

    private fun propertyViewModel(property: LimeProperty): Map<String, Any> =
        mapOf(
            "model" to property,
            "jsName" to nameRules.getName(property),
            "cppGetterName" to cppNameCache.getGetterName(property),
            "cppSetterName" to cppNameCache.getSetterName(property),
            "isStatic" to property.isStatic,
        )

    private fun fieldViewModel(struct: LimeStruct, field: LimeField): Map<String, Any?> =
        mapOf(
            "model" to field,
            "jsName" to nameRules.getName(field),
            "cppFullName" to cppNameCache.getFullyQualifiedName(struct),
            "cppType" to embindNameResolver.resolveName(field.typeRef),
            // Raw field name for `&Struct::field` pointer syntax; null when the field uses
            // external accessors (getter/setter registration is required then).
            "cppFieldName" to
                if (field.external?.cpp?.get(LimeExternalDescriptor.Companion.GETTER_NAME_NAME) != null) {
                    null
                } else {
                    field.path.tail.last()
                },
        )

    private fun enumeratorViewModel(enumerator: com.here.gluecodium.model.lime.LimeEnumerator): Map<String, Any> =
        mapOf(
            "model" to enumerator,
            "jsName" to nameRules.getName(enumerator),
            "cppName" to
                "${embindNameResolver.resolveFullName(getParentEnumeration(enumerator))}::${embindNameResolver.resolveName(enumerator)}",
        )

    private fun getParentEnumeration(enumerator: com.here.gluecodium.model.lime.LimeEnumerator): com.here.gluecodium.model.lime.LimeEnumeration =
        limeReferenceMap[enumerator.path.parent.toString()] as? com.here.gluecodium.model.lime.LimeEnumeration
            ?: throw IllegalStateException("Unable to resolve parent enumeration for ${enumerator.fullName}")

    private fun constantViewModel(constant: LimeConstant): Map<String, Any> =
        mapOf(
            "model" to constant,
            "jsName" to nameRules.getName(constant),
            "cppFullName" to cppNameCache.getFullyQualifiedName(constant),
        )

    /**
     * Recursively collects all types (top-level + nested) that should emit an embind binding,
     * in parent-before-child order. Excludes type aliases and lambdas (which emit no binding).
     */
    private fun collectEmbindTypes(limeType: com.here.gluecodium.model.lime.LimeType): List<com.here.gluecodium.model.lime.LimeType> {
        val result = mutableListOf<com.here.gluecodium.model.lime.LimeType>()
        if (limeType !is com.here.gluecodium.model.lime.LimeTypeAlias && limeType !is LimeLambda) {
            result.add(limeType)
        }
        val container = limeType as? com.here.gluecodium.model.lime.LimeContainer ?: return result
        val nestedTypes =
            container.structs + container.classes + container.interfaces +
                container.enumerations + container.exceptions +
                container.typeAliases + container.lambdas
        for (nested in nestedTypes) {
            result.addAll(collectEmbindTypes(nested))
        }
        return result
    }

    private fun generateCommonFiles(
        filteredModel: LimeModel,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        // Module init: aggregates every per-top-level-element register_* call inside one
        // EMSCRIPTEN_BINDINGS block, in dependency order (bases before derived types).
        val topLevelBoundTypes =
            filteredModel.topElements
                .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
                .filter { it !is com.here.gluecodium.model.lime.LimeTypeAlias && it !is LimeLambda }
        val registerNameToDeps =
            topLevelBoundTypes.associate { topType ->
                val topRegName = resolveRegisterName(topType)
                val deps =
                    collectEmbindTypes(topType)
                        .mapNotNull { it as? LimeContainerWithInheritance }
                        .flatMap { container ->
                            container.parents
                                .mapNotNull { it.type.actualType as? LimeNamedElement }
                                .filter { filteredModel.referenceMap.containsKey(it.fullName) }
                                .map { resolveRegisterName(findTopLevelElement(it)) }
                        }
                        .filter { it != topRegName }
                        .distinct()
                topRegName to deps
            }
        val moduleInitContent =
            TemplateEngine.render(
                "js/EmbindModuleInit",
                mapOf(
                    "moduleName" to jsModuleName,
                    "registerFunctions" to topologicalSort(registerNameToDeps).map { mapOf("name" to it) },
                    "genericRegistrations" to collectGenericRegistrations(filteredModel),
                ),
                nameResolvers,
            )
        return listOf(GeneratedFile(moduleInitContent, JsNameRules.MODULE_INIT_FILE))
    }

    private fun collectGenericRegistrations(filteredModel: LimeModel): List<Map<String, Any>> {
        val registrations = linkedMapOf<String, Map<String, Any>>()

        fun collect(typeRef: com.here.gluecodium.model.lime.LimeTypeRef) {
            when (val type = typeRef.type) {
                is LimeList -> {
                    collect(type.elementType)
                    val elementType = embindNameResolver.resolveName(type.elementType)
                    val name = "Vector_${sanitizeRegistrationName(elementType)}"
                    registrations.putIfAbsent(name, mapOf("vector" to true, "type" to elementType, "name" to name))
                }
                is LimeMap -> {
                    collect(type.keyType)
                    collect(type.valueType)
                }
                is LimeSet -> collect(type.elementType)
                else -> Unit
            }
            if (typeRef.isNullable) {
                val typeName = embindNameResolver.resolveName(typeRef.type)
                val name = "Optional_${sanitizeRegistrationName(typeName)}"
                registrations.putIfAbsent(name, mapOf("optional" to true, "type" to typeName, "name" to name))
            }
        }

        fun collectFromContainer(container: com.here.gluecodium.model.lime.LimeContainer) {
            container.functions.flatMap { it.parameters.map { parameter -> parameter.typeRef } + it.returnType.typeRef }.forEach(::collect)
            container.properties.map { it.typeRef }.forEach(::collect)
            container.constants.map { it.typeRef }.forEach(::collect)
            container.constructors.flatMap { constructor -> constructor.parameters.map { it.typeRef } }.forEach(::collect)
            (container as? LimeStruct)?.fields?.map { it.typeRef }?.forEach(::collect)
        }

        filteredModel.topElements
            .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
            .flatMap(::collectEmbindTypes)
            .forEach { type ->
                (type as? com.here.gluecodium.model.lime.LimeContainer)?.let(::collectFromContainer)
            }
        return registrations.values.toList()
    }

    private fun sanitizeRegistrationName(typeName: String) =
        typeName.replace(Regex("[^A-Za-z0-9_]"), "_").trim('_').ifEmpty { "Type" }

    private fun findTopLevelElement(element: LimeNamedElement): LimeNamedElement {
        var current = element
        while (current.path.hasParent) {
            val parent = limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement ?: return current
            current = parent
        }
        return current
    }

    private fun resolveRegisterName(limeElement: LimeNamedElement): String {
        val name = nameRules.getFlattenedName(limeElement)
        val packagePath = limeElement.path.head.joinToString("_")
        return if (packagePath.isNotEmpty()) "${packagePath}_$name" else name
    }

    // Topologically sorts register names so that every base class appears before its derived
    // classes. A stable sort is used for ties so the output stays deterministic.
    private fun topologicalSort(parents: Map<String, List<String>>): List<String> {
        val visited = mutableSetOf<String>()
        val result = mutableListOf<String>()

        fun visit(name: String) {
            if (name in visited) return
            visited.add(name)
            parents[name].orEmpty().forEach { visit(it) }
            result.add(name)
        }
        parents.keys.sorted().forEach { visit(it) }
        return result
    }

    private fun selectStubTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is com.here.gluecodium.model.lime.LimeTypeAlias -> "js/JsStubTypeAlias"
            is LimeException -> "js/JsStubException"
            is LimeLambda -> "js/JsStubLambda"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "js/JsStubEnumeration"
            is LimeStruct -> "js/JsStubStruct"
            is com.here.gluecodium.model.lime.LimeClass -> "js/JsStubClass"
            is com.here.gluecodium.model.lime.LimeInterface -> "js/JsStubInterface"
            else -> null
        }

    private fun selectEmbindTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is LimeException -> "js/EmbindException"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "js/EmbindEnum"
            is LimeStruct -> "js/EmbindStruct"
            is com.here.gluecodium.model.lime.LimeClass -> "js/EmbindClass"
            is com.here.gluecodium.model.lime.LimeInterface -> "js/EmbindInterface"
            else -> null
        }

    /**
     * `@Cpp(Skip)` may only be used on field constructors and constants. Such elements are
     * omitted from the generated C++ API, so the embind binding — which wraps that C++ API —
     * must omit them too, or the binding would fail to compile.
     */
    private fun isCppSkipped(element: LimeNamedElement) =
        (element is LimeFieldConstructor || element is com.here.gluecodium.model.lime.LimeConstant) &&
            element.attributes.have(LimeAttributeType.CPP, SKIP)

    companion object {
        private val logger = Logger.getLogger(JsGenerator::class.java.name)
    }
}
