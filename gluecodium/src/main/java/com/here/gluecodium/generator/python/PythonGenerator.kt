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
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeAttributeValueType.SKIP
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeHelper
import java.io.File
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
    private lateinit var pybind11NameResolver: Pybind11NameResolver
    private lateinit var cppNameCache: CppNameCache

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
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, PYTHON, retainFunctionsAndFields = true) &&
                    !isCppSkipped(it)
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

        cppNameCache = CppNameCache(rootNamespace, pybind11FilteredModel.referenceMap, cppNameRules)
        pybind11NameResolver =
            Pybind11NameResolver(
                pybind11FilteredModel.referenceMap,
                internalNamespace,
                cppNameCache,
                cppNameRules,
            )
        val nameResolvers =
            mapOf(
                "" to pythonNameResolver,
                "Pybind11" to pybind11NameResolver,
            )
        val pythonTypes = getPythonTypes(pythonFilteredModel.topElements)
        val pybind11Types = getPythonTypes(pybind11FilteredModel.topElements)
        val predicates =
            PythonGeneratorPredicates(
                limeOverloadsValidatorSignatureResolver(pybind11FilteredModel),
                pythonFilteredModel.referenceMap,
                pybind11NameResolver,
                pythonTypes.filterIsInstance<LimeEnumeration>().map { it.fullName }.toSet(),
            )

        val pybind11IncludeResolver = Pybind11IncludeResolver(pybind11FilteredModel.referenceMap, cppNameRules, internalNamespace)
        val pybind11IncludeCollector =
            GenericIncludesCollector(
                pybind11IncludeResolver,
                retainPredicate = { predicates.predicates["isPublic"]!!.invoke(it) },
            )

        val pythonFiles =
            pythonTypes.flatMap {
                generatePythonFile(it, nameResolvers, predicates.predicates)
            }
        val pybind11Files =
            pybind11Types.flatMap {
                generatePybind11File(it, nameResolvers, pybind11IncludeCollector, predicates.predicates)
            }

        if (commentsProcessor.hasError) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        return pythonFiles + pybind11Files +
            generateCommonFiles(pybind11FilteredModel, pythonFilteredModel, nameResolvers, predicates.predicates)
    }

    private fun generatePythonFile(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        predicates: Map<String, (Any) -> Boolean>,
    ): List<GeneratedFile> {
        // Drop the self-import: a type that references itself (e.g. `Greeter.create()` returns
        // `Greeter`) would otherwise emit `from ...Greeter import Greeter` inside Greeter.py,
        // which is a circular import and breaks direct importability of the wrapper.
        val selfModulePath = (limeElement.path.head + pythonNameResolver.resolveName(limeElement)).joinToString(".")
        // Types that are an ancestor of the current element's own container (e.g. a nested struct
        // field pointing back to its enclosing class, or a nested class `build()` returning its
        // enclosing struct) are imported locally inside the property getter / function body instead
        // (see PythonField.mustache / PythonFunction.mustache), to avoid an unresolvable circular
        // import between the two flattened top-level modules.
        val ancestorModulePaths =
            when (limeElement) {
                is com.here.gluecodium.model.lime.LimeStruct ->
                    limeElement.fields
                        .filter { predicates["isAncestorField"]?.invoke(it) == true }
                        .mapNotNull { pythonNameResolver.resolveReferenceName(it.typeRef) }
                is com.here.gluecodium.model.lime.LimeClass ->
                    (limeElement.functions.filter { predicates["isAncestorReturnType"]?.invoke(it) == true }
                        .mapNotNull { pythonNameResolver.resolveReferenceName(it.returnType.typeRef) } +
                        limeElement.properties.filter { predicates["isAncestorProperty"]?.invoke(it) == true }
                            .mapNotNull { pythonNameResolver.resolveReferenceName(it.typeRef) })
                is com.here.gluecodium.model.lime.LimeInterface ->
                    (limeElement.functions.filter { predicates["isAncestorReturnType"]?.invoke(it) == true }
                        .mapNotNull { pythonNameResolver.resolveReferenceName(it.returnType.typeRef) } +
                        limeElement.properties.filter { predicates["isAncestorProperty"]?.invoke(it) == true }
                            .mapNotNull { pythonNameResolver.resolveReferenceName(it.typeRef) })
                else -> emptyList()
            }.toSet()
        // A parent type must not import its own nested children at module level. The imports
        // collector walks the whole nested subtree, so a child's self-reference (e.g.
        // `Builder.field(): Builder`) or a child referenced by a nested exception (`exception
        // Instantiation(InnerEnum)`) would otherwise pull the child module into the parent and
        // create a circular import (`OuterStruct` <-> `Builder`). Children are referenced only
        // through their flattened top-level names, which are always available without an import.
        // We derive the child module paths from the LIME model's own descendants (not the
        // flattened `pythonTypes` list, which may drop some children due to filename collisions)
        // so every nested child is reliably excluded.
        val childModulePaths =
            LimeTypeHelper.getAllTypes(limeElement)
                .filter { it != limeElement && it.path.allParents.contains(limeElement.path) }
                .mapNotNull { pythonNameResolver.resolveReferenceName(it) }
                .toSet()
        val imports =
            pythonImportsCollector.collectImports(limeElement)
                .filterNot { it.modulePath == selfModulePath }
                .filterNot { it.modulePath in ancestorModulePaths }
                .filterNot { it.modulePath in childModulePaths }
                .distinct()
                .sorted()
        val templateData =
            mapOf(
                "model" to limeElement,
                "imports" to imports,
                "moduleName" to pythonModule,
                "nativeModule" to pythonModule,
                "typeName" to pythonNameResolver.resolveName(limeElement),
                "nativeTypeName" to pythonNameResolver.resolveName(limeElement),
                "contentTemplate" to selectPythonTemplate(limeElement),
            )
        val content = TemplateEngine.render("python/PythonFile", templateData, nameResolvers, predicates)
        val stubContent = TemplateEngine.render("python/PythonStub", templateData, nameResolvers, predicates)
        return listOf(
            GeneratedFile(content, nameRules.getPythonFileName(limeElement)),
            GeneratedFile(stubContent, nameRules.getPythonStubFileName(limeElement)),
        )
    }

    private fun generatePybind11File(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        includeCollector: GenericIncludesCollector,
        predicates: Map<String, (Any) -> Boolean>,
    ): List<GeneratedFile> {
        val limeType = limeElement as? com.here.gluecodium.model.lime.LimeType ?: return emptyList()
        // Exceptions are represented as std::error_code in C++ (no dedicated header is generated),
        // so the include collector would resolve a non-existent header. The exception translator
        // only needs the common pybind11 headers, so we skip per-element includes for exceptions.
        val includes =
            if (limeType is com.here.gluecodium.model.lime.LimeException) {
                emptyList()
            } else {
                includeCollector.collectImports(limeType).distinct().sorted()
            }
        val templateData =
            mapOf(
                "model" to limeElement,
                "moduleName" to pythonModule,
                "includes" to includes,
                "internalNamespace" to internalNamespace,
                "fullName" to
                    if (limeType is com.here.gluecodium.model.lime.LimeException) {
                        ""
                    } else {
                        cppNameCache.getFullyQualifiedName(limeElement)
                    },
                "returnTypeFullName" to (internalNamespace + "Return").joinToString("::"),
                "trampolineName" to (pythonNameResolver.resolveName(limeElement) + "Trampoline"),
                "contentTemplate" to selectPybind11Template(limeElement),
            )
        val content = TemplateEngine.render("python/Pybind11File", templateData, nameResolvers, predicates)
        return listOf(GeneratedFile(content, nameRules.getPybind11FileName(limeElement)))
    }

    private fun generateCommonFiles(
        pybind11FilteredModel: LimeModel,
        pythonFilteredModel: LimeModel,
        nameResolvers: Map<String, NameResolver>,
        predicates: Map<String, (Any) -> Boolean>,
    ): List<GeneratedFile> {
        val initTemplateData = mapOf("moduleName" to pythonModule)
        val initContent = TemplateEngine.render("python/PythonInit", initTemplateData, nameResolvers, predicates)

        // Custom type caster for Gluecodium's Return<T, Error> adapter. The include path for the
        // generated Return.h follows the C++ internal namespace (e.g. "lorem_ipsum/Return.h").
        val returnInclude = (internalNamespace + "Return.h").joinToString("/")
        val casterTemplateData =
            mapOf(
                "returnInclude" to returnInclude,
                "returnTypeFullName" to (internalNamespace + "Return").joinToString("::"),
            )
        val casterContent =
            TemplateEngine.render("python/Pybind11ReturnCaster", casterTemplateData, nameResolvers, predicates)

        // Wrapper cache: preserves referential equality across the C++ <-> Python boundary by
        // mapping a C++ instance pointer to a single Python wrapper object.
        val wrapperCacheContent =
            TemplateEngine.render("python/Pybind11WrapperCache", emptyMap<String, Any>(), nameResolvers, predicates)

        // Module entry point: aggregates every per-type register_* function into a single
        // PYBIND11_MODULE. Type aliases and lambdas emit no binding, so they are excluded.
        val registerFunctions =
            getPythonTypes(pybind11FilteredModel.topElements)
                .filter { it !is com.here.gluecodium.model.lime.LimeTypeAlias && it !is com.here.gluecodium.model.lime.LimeLambda }
                .map { pythonNameResolver.resolveName(it) }
                .sorted()
        val moduleInitTemplateData =
            mapOf(
                "moduleName" to pythonModule,
                "moduleDoc" to "Generated Python bindings for the '$pythonModule' extension module.",
                "registerFunctions" to registerFunctions.map { mapOf("name" to it) },
            )
        val moduleInitContent =
            TemplateEngine.render("python/Pybind11ModuleInit", moduleInitTemplateData, nameResolvers, predicates)

        // Common Python build/helper files.
        val setupPyContent = TemplateEngine.render("python/PythonSetupPy", mapOf("moduleName" to pythonModule), nameResolvers, predicates)
        val pyprojectContent =
            TemplateEngine.render(
                "python/PythonPyproject",
                mapOf("moduleName" to pythonModule),
                nameResolvers,
                predicates,
            )
        val nativeBaseContent = TemplateEngine.render("python/PythonNativeBase", emptyMap<String, Any>(), nameResolvers, predicates)

        // Per-package __init__.py files so the generated wrappers form an importable package
        // hierarchy (e.g. com/__init__.py, com/example/__init__.py, com/example/greeter/__init__.py).
        // Without these, `import com.example.greeter.Greeter` fails with ModuleNotFoundError.
        val packageInitFiles =
            pythonFilteredModel.topElements
                .flatMap { it.path.head }
                .distinct()
                .map { PythonNameRules.PYTHON_TARGET_DIRECTORY + it + File.separator + "__init__.py" }
                .map { GeneratedFile(initContent, it) }
                .toList()

        return listOf(
            GeneratedFile(initContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "__init__.py"),
            GeneratedFile(casterContent, PythonNameRules.PYBIND11_TARGET_DIRECTORY + "_return_caster.h"),
            GeneratedFile(wrapperCacheContent, PythonNameRules.PYBIND11_TARGET_DIRECTORY + "_wrapper_cache.h"),
            GeneratedFile(moduleInitContent, PythonNameRules.MODULE_INIT_FILE),
            GeneratedFile(setupPyContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "setup.py"),
            GeneratedFile(pyprojectContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "pyproject.toml"),
            GeneratedFile(nativeBaseContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "_native_base.py"),
        ) + packageInitFiles
    }

    private fun getPythonTypes(elements: List<LimeNamedElement>): List<LimeType> =
        elements.flatMap { element ->
            val topType = element as? LimeType ?: return@flatMap emptyList()
            listOf(topType) +
                LimeTypeHelper.getAllTypes(topType)
                    .filter {
                        it is LimeEnumeration ||
                            it is com.here.gluecodium.model.lime.LimeStruct ||
                            it is com.here.gluecodium.model.lime.LimeClass ||
                            it is com.here.gluecodium.model.lime.LimeInterface ||
                            it is com.here.gluecodium.model.lime.LimeLambda
                    }.filter { it != topType }
        }.distinctBy { it.fullName }
            .let { types ->
                val duplicateFileNames =
                    types.groupingBy { nameRules.getPythonFileName(it) }
                        .eachCount()
                        .filterValues { it > 1 }
                        .keys
                types.filter {
                    (
                        it !is LimeEnumeration &&
                            it !is com.here.gluecodium.model.lime.LimeStruct &&
                            it !is com.here.gluecodium.model.lime.LimeClass &&
                            it !is com.here.gluecodium.model.lime.LimeInterface &&
                            it !is com.here.gluecodium.model.lime.LimeLambda
                    ) ||
                        nameRules.getPythonFileName(it) !in duplicateFileNames
                }
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

    private fun limeOverloadsValidatorSignatureResolver(model: LimeModel) =
        com.here.gluecodium.model.lime.LimeSignatureResolver(model.referenceMap)

    /**
     * `@Cpp(Skip)` may only be used on field constructors and constants (see
     * [com.here.gluecodium.generator.cpp.CppSkipAttributesValidator]). Such elements are omitted from
     * the generated C++ API, so the pybind11 binding — which wraps that C++ API — must omit them too.
     * Without this, pybind11 would emit `py::init<...>()` for a constructor that does not exist in C++,
     * which fails to compile.
     */
    private fun isCppSkipped(element: LimeNamedElement) =
        (element is LimeFieldConstructor || element is LimeConstant) &&
            element.attributes.have(LimeAttributeType.CPP, SKIP)

    companion object {
        private val logger = Logger.getLogger(PythonGenerator::class.java.name)
    }
}
