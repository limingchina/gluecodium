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
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.generator.cpp.CppSignatureResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.ACCESSORS
import com.here.gluecodium.model.lime.LimeAttributeValueType.SKIP
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeDirectTypeRef
import com.here.gluecodium.model.lime.LimeBasicType.TypeId
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
    private var emitTypeScriptStubs = true

    private lateinit var limeReferenceMap: Map<String, LimeElement>
    private lateinit var jsNameResolver: JsNameResolver
    private lateinit var embindNameResolver: EmbindNameResolver
    private lateinit var cppNameCache: CppNameCache
    private lateinit var conversions: EmbindConversionEmitter
    private lateinit var embindViewModelBuilder: JsEmbindViewModelBuilder
    private lateinit var embindFileGenerator: JsEmbindFileGenerator

    override val shortName = "js"

    override fun initialize(options: GeneratorOptions) {
        internalNamespace = options.cppInternalNamespace
        rootNamespace = options.cppRootNamespace
        commentsProcessor = JsCommentsProcessor(options.werror.contains(GeneratorOptions.WARNING_DOC_LINKS))
        cppNameRules = CppNameRules(rootNamespace, nameRuleSetFromConfig(options.cppNameRules))
        nameRules = JsNameRules(nameRuleSetFromConfig(options.jsNameRules))
        jsModuleName = options.jsModuleName
        activeTags = options.tags
        emitTypeScriptStubs = options.jsEmitTypeScriptStubs
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
        conversions =
            EmbindConversionEmitter(embindNameResolver, cppNameCache, nameRules)
        embindViewModelBuilder =
            JsEmbindViewModelBuilder(
                internalNamespace = internalNamespace,
                referenceMap = limeReferenceMap,
                nameRules = nameRules,
                cppNameRules = cppNameRules,
                embindNameResolver = embindNameResolver,
                cppNameCache = cppNameCache,
                conversions = conversions,
                resolveRegisterName = ::resolveRegisterName,
                primaryBaseType = ::primaryBaseType,
                secondaryParentMembers = ::secondaryParentMembers,
                primaryInheritedOverloads = ::primaryInheritedOverloads,
                isSupportedConstant = ::isSupportedConstant,
            )
        embindFileGenerator =
            JsEmbindFileGenerator(
                internalNamespace = internalNamespace,
                referenceMap = limeReferenceMap,
                cppNameRules = cppNameRules,
                nameRules = nameRules,
                embindViewModelBuilder = embindViewModelBuilder,
                resolveRegisterName = ::resolveRegisterName,
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
            if (emitTypeScriptStubs) {
                JsStubGenerator(
                    nameRules,
                    jsNameResolver,
                    jsModuleName,
                    importsCollector,
                    nameResolvers,
                ).generate(jsFilteredModel.topElements.filterIsInstance<LimeNamedElement>())
            } else {
                emptyList()
            }
        val embindFiles =
            embindFilteredModel.topElements.flatMap {
                embindFileGenerator.generate(it, nameResolvers, embindFilteredModel)
            }

        if (commentsProcessor.hasError) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        return stubFiles + embindFiles +
            generateCommonFiles(embindFilteredModel, jsFilteredModel, nameResolvers)
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

    private fun primaryInheritedOverloads(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): List<LimeFunction> {
        val container = type as? LimeContainerWithInheritance ?: return emptyList()
        val primaryBase = primaryBaseType(type, filteredModel) ?: return emptyList()
        val ownNames = container.functions
            .filterNot { it.isStatic || it.isConstructor }
            .map { nameRules.getName(it) }
            .toSet()
        if (ownNames.isEmpty()) return emptyList()
        return (primaryBase.functions + primaryBase.inheritedFunctions)
            .filter { !it.isStatic && nameRules.getName(it) in ownNames }
            .distinctBy { it.fullName }
    }

    private fun generateCommonFiles(
        filteredModel: LimeModel,
        jsFilteredModel: LimeModel,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        // Module init: aggregates every per-top-level-element register_* call inside one
        // EMSCRIPTEN_BINDINGS block, in dependency order (bases before derived types).
        val topLevelBoundTypes =
            filteredModel.topElements
                .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
                .filter { it !is com.here.gluecodium.model.lime.LimeTypeAlias && it !is LimeLambda }
        val boundTypes = topLevelBoundTypes.flatMap(embindFileGenerator::collectTypes)
        val boundTypeNames = boundTypes.map(::resolveRegisterName).toSet()
        val registerNameToDeps =
            boundTypes.associate { type ->
                val registerName = resolveRegisterName(type)
                val nestedTypeDeps =
                    if (type in topLevelBoundTypes) {
                        embindFileGenerator.collectTypes(type).drop(1).map(::resolveRegisterName)
                    } else {
                        emptyList()
                    }
                val parentDeps =
                    (type as? LimeContainerWithInheritance)?.parents
                        ?.mapNotNull { it.type.actualType }
                        ?.map(::resolveRegisterName)
                        .orEmpty()
                registerName to (nestedTypeDeps + parentDeps)
                    .filter { it != registerName && it in boundTypeNames }
                    .distinct()
            }
        val genericRegistrations =
            JsGenericRegistrationCollector(
                referenceMap = limeReferenceMap,
                cppNameRules = cppNameRules,
                internalNamespace = internalNamespace,
                embindNameResolver = embindNameResolver,
                requiresJsAdapter = conversions::requiresJsAdapter,
                collectEmbindTypes = embindFileGenerator::collectTypes,
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
                .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
                .flatMap(embindFileGenerator::collectTypes)
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
                collectEmbindTypes = embindFileGenerator::collectTypes,
                isSupportedConstant = ::isSupportedConstant,
                isCppSkipped = ::isCppSkipped,
                propertyAdapterName = embindViewModelBuilder::propertyAdapterName,
                overloadRuntimeName = embindViewModelBuilder::overloadRuntimeName,
                structFunctionRuntimeName = embindViewModelBuilder::structFunctionRuntimeName,
                overloadPredicate = embindViewModelBuilder::overloadPredicate,
                instanceOverloadGroups = ::instanceOverloadGroups,
            ).generate(jsFilteredModel)
        return packageFiles + listOf(
            GeneratedFile(moduleInitContent, JsNameRules.MODULE_INIT_FILE),
            GeneratedFile(wrapperRuntimeContent, JsNameRules.WRAPPER_RUNTIME_FILE),
            GeneratedFile(moduleRuntimeContent, JsNameRules.MODULE_RUNTIME_FILE),
        )
    }

    private fun containsNullableSet(filteredModel: LimeModel): Boolean {
        fun contains(typeRef: com.here.gluecodium.model.lime.LimeTypeRef): Boolean {
            val type = typeRef.type
            if (typeRef.isNullable && type.actualType is LimeSet) return true
            return type.childTypes.any(::contains)
        }

        return filteredModel.topElements
            .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
            .flatMap(embindFileGenerator::collectTypes)
            .filterIsInstance<com.here.gluecodium.model.lime.LimeContainer>()
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

    private fun sanitizeRegistrationName(typeName: String) =
        typeName.replace(Regex("[^A-Za-z0-9_]"), "_").trim('_').ifEmpty { "Type" }

    private fun resolveRegisterName(limeElement: LimeNamedElement): String {
        val name = nameRules.getFlattenedName(limeElement)
        val packagePath = limeElement.path.head.joinToString("_")
        return if (packagePath.isNotEmpty()) "${packagePath}_$name" else name
    }

    private fun instanceOverloadGroups(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): List<Map<String, Any>> {
        val container = type as? com.here.gluecodium.model.lime.LimeContainer ?: return emptyList()
        val (secondaryFunctions, _) = secondaryParentMembers(type, filteredModel)
        val functions =
            (primaryInheritedOverloads(type, filteredModel) +
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
                            "runtimeName" to embindViewModelBuilder.overloadRuntimeName(function),
                            "predicate" to embindViewModelBuilder.overloadPredicate(function),
                        )
                    },
                )
            }
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

    private fun isSupportedConstant(constant: LimeConstant) =
        when (constant.typeRef.type.actualType) {
            is LimeList, is LimeSet, is LimeMap -> false
            else -> true
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
