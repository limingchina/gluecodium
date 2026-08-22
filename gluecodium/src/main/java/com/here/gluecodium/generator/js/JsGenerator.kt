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
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.SKIP
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
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
                    "content" to "",
                    "nestedTypes" to "",
                ),
                nameResolvers,
            )
        return listOf(GeneratedFile(content, nameRules.getJsStubFileName(limeElement)))
    }

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
                    mapOf(
                        "model" to type,
                        "internalNamespace" to internalNamespace,
                        "jsName" to nameRules.getName(type),
                        "cppFullName" to cppNameCache.getFullyQualifiedName(type),
                        "primaryBase" to primaryBaseOf(type, filteredModel),
                    ),
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
    ): Map<String, String>? =
        (type as? LimeContainerWithInheritance)?.parents
            ?.mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
            ?.filter { filteredModel.referenceMap.containsKey(it.fullName) }
            ?.minByOrNull { it is com.here.gluecodium.model.lime.LimeInterface }
            ?.let { mapOf("fqn" to cppNameCache.getFullyQualifiedName(it)) }

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
                ),
                nameResolvers,
            )
        return listOf(GeneratedFile(moduleInitContent, JsNameRules.MODULE_INIT_FILE))
    }

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
