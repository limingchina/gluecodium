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
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeTypeHelper
import com.here.gluecodium.validator.LimeOverloadsValidator
import java.util.logging.Logger

/**
 * Generates Python bindings on top of the C++ API using pybind11.
 *
 * <p>Architecturally this mirrors the Swift generator: it produces Python source files plus
 * pybind11 C++ binding files that `#include` the generated C++ headers and call the C++ API
 * directly (there is no intermediate C-ABI shim, unlike the Dart FFI generator).
 */
internal class PythonGenerator : Generator {
    private lateinit var internalNamespace: List<String>
    private lateinit var rootNamespace: List<String>
    private lateinit var commentsProcessor: PythonCommentsProcessor
    private lateinit var cppNameRules: CppNameRules
    private lateinit var nameRules: PythonNameRules
    private lateinit var pythonModule: String
    private lateinit var activeTags: Set<String>
    private var overloadsWerror: Boolean = false

    private val pythonImportsCollector by lazy {
        GenericImportsCollector(
            PythonImportResolver(limeReferenceMap, pythonNameResolver),
            collectTypeRefImports = true,
            collectValueImports = true,
            parentTypeFilter = { true },
            collectTypeAliasImports = true,
        )
    }

    private lateinit var limeReferenceMap: Map<String, com.here.gluecodium.model.lime.LimeElement>
    private lateinit var pythonNameResolver: PythonNameResolver

    override val shortName = "python"

    override fun initialize(options: GeneratorOptions) {
        internalNamespace = options.cppInternalNamespace
        rootNamespace = options.cppRootNamespace
        commentsProcessor = PythonCommentsProcessor(options.werror.contains(GeneratorOptions.WARNING_DOC_LINKS))
        cppNameRules = CppNameRules(rootNamespace, nameRuleSetFromConfig(options.cppNameRules))
        nameRules = PythonNameRules(nameRuleSetFromConfig(options.pythonNameRules))
        pythonModule = options.pythonModule
        overloadsWerror = options.werror.contains(GeneratorOptions.WARNING_PYTHON_OVERLOADS)
        activeTags = options.tags
    }

    override fun generate(limeModel: LimeModel): List<GeneratedFile> {
        limeReferenceMap = limeModel.referenceMap
        val limeLogger = LimeLogger(logger, limeModel.fileNameMap)

        // Filter the model: keep elements that are not skipped for Python. The first pass retains
        // functions/fields (needed for container bodies); the second pass drops them for the
        // actual Python output.
        val pybind11FilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, PYTHON, retainFunctionsAndFields = true)
            }
        val pythonFilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, PYTHON, retainFunctionsAndFields = false)
            }

        pythonNameResolver =
            PythonNameResolver(pybind11FilteredModel.referenceMap, nameRules, limeLogger, commentsProcessor)

        val overloadsValidationResult =
            PythonOverloadsValidator(pythonNameResolver, limeLogger, overloadsWerror)
                .validate(pythonFilteredModel.referenceMap.values)
        if (!overloadsValidationResult) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        val nameResolvers =
            mapOf(
                "" to pythonNameResolver,
                "Pybind11" to
                    Pybind11NameResolver(
                        pybind11FilteredModel.referenceMap,
                        internalNamespace,
                        CppNameCache(rootNamespace, pybind11FilteredModel.referenceMap, cppNameRules),
                        cppNameRules,
                    ),
            )
        val predicates = PythonGeneratorPredicates(LimeOverloadsValidatorSignatureResolver(pybind11FilteredModel), pythonFilteredModel.referenceMap)

        val pybind11IncludeResolver = Pybind11IncludeResolver(pybind11FilteredModel.referenceMap, cppNameRules, internalNamespace)
        val pybind11IncludeCollector =
            GenericIncludesCollector(
                pybind11IncludeResolver,
                retainPredicate = { predicates.predicates["isPublic"]!!.invoke(it) },
            )

        val pythonFiles =
            pythonFilteredModel.topElements.map {
                generatePythonFile(it, nameResolvers, predicates.predicates)
            }
        val pybind11Files =
            pybind11FilteredModel.topElements.flatMap {
                generatePybind11File(it, nameResolvers, pybind11IncludeCollector, predicates.predicates)
            }

        if (commentsProcessor.hasError) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        return pythonFiles + pybind11Files + generateCommonFiles(nameResolvers, predicates.predicates)
    }

    private fun generatePythonFile(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        predicates: Map<String, (Any) -> Boolean>,
    ): GeneratedFile {
        val imports = pythonImportsCollector.collectImports(limeElement)
        val templateData =
            mapOf(
                "model" to limeElement,
                "imports" to imports.distinct().sorted(),
                "moduleName" to pythonModule,
                "contentTemplate" to selectPythonTemplate(limeElement),
            )
        val content = TemplateEngine.render("python/PythonFile", templateData, nameResolvers, predicates)
        return GeneratedFile(content, nameRules.getPythonFileName(limeElement))
    }

    private fun generatePybind11File(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        includeCollector: GenericIncludesCollector,
        predicates: Map<String, (Any) -> Boolean>,
    ): List<GeneratedFile> {
        val limeType = limeElement as? com.here.gluecodium.model.lime.LimeType ?: return emptyList()
        val includes = includeCollector.collectImports(limeType).distinct().sorted()
        val templateData =
            mapOf(
                "model" to limeElement,
                "moduleName" to pythonModule,
                "includes" to includes,
                "contentTemplate" to selectPybind11Template(limeElement),
            )
        val content = TemplateEngine.render("python/Pybind11File", templateData, nameResolvers, predicates)
        return listOf(GeneratedFile(content, nameRules.getPybind11FileName(limeElement)))
    }

    private fun generateCommonFiles(
        nameResolvers: Map<String, NameResolver>,
        predicates: Map<String, (Any) -> Boolean>,
    ): List<GeneratedFile> {
        val initTemplateData = mapOf("moduleName" to pythonModule)
        val initContent = TemplateEngine.render("python/PythonInit", initTemplateData, nameResolvers, predicates)
        return listOf(GeneratedFile(initContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "__init__.py"))
    }

    private fun selectPythonTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is com.here.gluecodium.model.lime.LimeTypeAlias -> "python/PythonTypeAlias"
            is com.here.gluecodium.model.lime.LimeException -> "python/PythonException"
            is com.here.gluecodium.model.lime.LimeLambda -> "python/PythonLambda"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "python/PythonEnumeration"
            is com.here.gluecodium.model.lime.LimeStruct -> "python/PythonStruct"
            is com.here.gluecodium.model.lime.LimeClass -> "python/PythonClass"
            is com.here.gluecodium.model.lime.LimeInterface -> "python/PythonInterface"
            else -> null
        }

    private fun selectPybind11Template(limeElement: LimeNamedElement) =
        when (limeElement) {
            is com.here.gluecodium.model.lime.LimeTypeAlias -> "python/Pybind11TypeAlias"
            is com.here.gluecodium.model.lime.LimeException -> "python/Pybind11Exception"
            is com.here.gluecodium.model.lime.LimeLambda -> "python/Pybind11Lambda"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "python/Pybind11Enum"
            is com.here.gluecodium.model.lime.LimeStruct -> "python/Pybind11Struct"
            is com.here.gluecodium.model.lime.LimeClass -> "python/Pybind11Class"
            is com.here.gluecodium.model.lime.LimeInterface -> "python/Pybind11Interface"
            else -> null
        }

    private fun LimeOverloadsValidatorSignatureResolver(model: LimeModel) =
        com.here.gluecodium.model.lime.LimeSignatureResolver(model.referenceMap)

    companion object {
        private val logger = Logger.getLogger(PythonGenerator::class.java.name)
    }
}
