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
import com.here.gluecodium.generator.common.GeneratedFile
import com.here.gluecodium.generator.common.Generator
import com.here.gluecodium.generator.common.GeneratorOptions
import com.here.gluecodium.generator.common.nameRuleSetFromConfig
import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.generator.cpp.CppSignatureResolver
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.ACCESSORS
import com.here.gluecodium.model.lime.LimeAttributeValueType.SKIP
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSet
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
    private lateinit var commonFileGenerator: JsCommonFileGenerator
    private lateinit var inheritanceResolver: JsInheritanceResolver
    private lateinit var overloadGroupGenerator: JsOverloadGroupGenerator
    private lateinit var outputGenerator: JsOutputGenerator

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

        val filteredModels = JsModelFilter(activeTags, ::isCppSkipped).filter(limeModel)
        val embindFilteredModel = filteredModels.embind
        val jsFilteredModel = filteredModels.stubs
        val constantsByCanonicalName = embindFilteredModel.referenceMap.values
            .filterIsInstance<LimeConstant>()
            .distinctBy { it.fullName }
            .groupingBy { it.path.toAmbiguousString() }
            .eachCount()
        val constantRuntimeNames = embindFilteredModel.referenceMap.values
            .filterIsInstance<LimeConstant>()
            .distinctBy { it.fullName }
            .associate { constant ->
                val canonicalName = constant.path.toAmbiguousString()
                val runtimeName = if (constantsByCanonicalName[canonicalName] == 1) canonicalName else constant.fullName
                constant.fullName to "gluecodium_constant_${runtimeName.replace(Regex("[^A-Za-z0-9_]"), "_")}"
            }

        jsNameResolver = JsNameResolver(embindFilteredModel.referenceMap, nameRules, limeLogger, commentsProcessor)

        limeReferenceMap = embindFilteredModel.referenceMap

        cppNameCache = CppNameCache(rootNamespace, embindFilteredModel.referenceMap, cppNameRules)
        embindNameResolver =
            EmbindNameResolver(
                embindFilteredModel.referenceMap,
                internalNamespace,
                cppNameCache,
            )
        conversions =
            EmbindConversionEmitter(embindNameResolver, cppNameCache, nameRules)
        inheritanceResolver = JsInheritanceResolver(nameRules, cppNameCache)
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
                primaryBaseType = inheritanceResolver::primaryBaseType,
                secondaryParentMembers = inheritanceResolver::secondaryParentMembers,
                primaryInheritedOverloads = inheritanceResolver::primaryInheritedOverloads,
                isSupportedConstant = ::isSupportedConstant,
                constantRuntimeName = { constant -> constantRuntimeNames.getValue(constant.fullName) },
            )
        overloadGroupGenerator =
            JsOverloadGroupGenerator(
                nameRules = nameRules,
                inheritanceResolver = inheritanceResolver,
                overloadRuntimeName = embindViewModelBuilder::overloadRuntimeName,
                overloadPredicate = embindViewModelBuilder::overloadPredicate,
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
        commonFileGenerator =
            JsCommonFileGenerator(
                internalNamespace = internalNamespace,
                referenceMap = limeReferenceMap,
                cppNameRules = cppNameRules,
                embindNameResolver = embindNameResolver,
                requiresJsAdapter = conversions::requiresJsAdapter,
                collectEmbindTypes = embindFileGenerator::collectTypes,
                resolveRegisterName = ::resolveRegisterName,
                nameRules = nameRules,
                jsModuleName = jsModuleName,
                emitTypeScriptStubs = emitTypeScriptStubs,
                isSupportedConstant = ::isSupportedConstant,
                isCppSkipped = ::isCppSkipped,
                constantRuntimeName = { constant -> constantRuntimeNames.getValue(constant.fullName) },
                propertyAdapterName = embindViewModelBuilder::propertyAdapterName,
                overloadRuntimeName = embindViewModelBuilder::overloadRuntimeName,
                structFunctionRuntimeName = embindViewModelBuilder::structFunctionRuntimeName,
                overloadPredicate = embindViewModelBuilder::overloadPredicate,
                instanceOverloadGroups = overloadGroupGenerator::generate,
            )
        outputGenerator =
            JsOutputGenerator(
                nameRules = nameRules,
                jsNameResolver = jsNameResolver,
                embindNameResolver = embindNameResolver,
                jsModuleName = jsModuleName,
                emitTypeScriptStubs = emitTypeScriptStubs,
                isSupportedConstant = ::isSupportedConstant,
                isCppSkipped = ::isCppSkipped,
                referenceMap = limeReferenceMap,
                embindFileGenerator = embindFileGenerator,
                commonFileGenerator = commonFileGenerator,
            )

        if (commentsProcessor.hasError) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        return outputGenerator.generate(embindFilteredModel, jsFilteredModel)
    }

    private fun resolveRegisterName(limeElement: LimeNamedElement): String {
        val name = nameRules.getFlattenedName(limeElement)
        val packagePath = limeElement.path.head.joinToString("_")
        return if (packagePath.isNotEmpty()) "${packagePath}_$name" else name
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
