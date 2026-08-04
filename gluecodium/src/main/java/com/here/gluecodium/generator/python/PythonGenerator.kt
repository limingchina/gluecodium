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
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeGenericType
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSignatureResolver
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeHelper
import com.here.gluecodium.model.lime.LimeTypeRef
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

    private lateinit var limeReferenceMap: Map<String, com.here.gluecodium.model.lime.LimeElement>
    private lateinit var pythonNameResolver: PythonNameResolver
    private lateinit var pythonImportsCollector: GenericImportsCollector<PythonImport>
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
        val limeLogger = LimeLogger(logger, limeModel.fileNameMap)

        // Filter the model: keep elements that are not skipped for Python. The first pass retains
        // functions/fields (needed for container bodies); the second pass drops them for the
        // actual Python output.
        // External types (those with `external { cpp include ...; cpp name ... }`) are pre-existing
        // C++ types. Unlike the C++ generator, the Python (pybind11) generator does NOT skip them:
        // it binds them by emitting a pybind11 `py::class_` that references the external C++ type
        // directly (via the external `cpp name`) and `#include`s the external header (via `cpp
        // include`). The existing C++ name/include resolvers already resolve these descriptors, so
        // the binding is correct. Skipping them would leave referencing types (e.g. a function
        // returning an external struct) with an unimportable Python module.
        val pybind11FilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, PYTHON, retainFunctionsAndFields = true) &&
                    !isCppSkipped(it)
            }
        // Filter the model for the actual Python output. Unlike the pybind11 model, this one
        // drops functions/fields individually (retainFunctionsAndFields = false). Internal
        // (@Internal) elements are NOT filtered out: they are retained and their names are
        // prefixed with a leading underscore (_) by PythonNameRules, following PEP 8's
        // convention for non-public API. This keeps internal members reachable (as they
        // may be relied upon by other generated code or same-package callers) while clearly
        // signaling non-public intent.
        val pythonFilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, PYTHON, retainFunctionsAndFields = false)
            }

        pythonNameResolver =
            PythonNameResolver(pybind11FilteredModel.referenceMap, nameRules, limeLogger, commentsProcessor)

        // Use the pybind11-filtered reference map (which retains @Internal elements) for import
        // resolution. The filtered map contains all parent elements registered by
        // LimeModelFilter.remap(), while the original model's map may not have top-level
        // container entries needed by findTopLevelElement() in PythonImportResolver.
        limeReferenceMap = pybind11FilteredModel.referenceMap

        // Create the imports collector fresh each time generate() is called. The Generator
        // instance is reused across smoke tests via ServiceLoader, so a lazy delegate would
        // capture the first test's reference map and never update.
        pythonImportsCollector =
            GenericImportsCollector(
                PythonImportResolver(limeReferenceMap, pythonNameResolver),
                collectTypeRefImports = true,
                collectValueImports = true,
                parentTypeFilter = { true },
                collectTypeAliasImports = true,
            )

        cppNameCache = CppNameCache(rootNamespace, pybind11FilteredModel.referenceMap, cppNameRules)
        pybind11NameResolver =
            Pybind11NameResolver(
                pybind11FilteredModel.referenceMap,
                internalNamespace,
                cppNameCache,
                cppNameRules,
            )
        val signatureResolver = LimeSignatureResolver(pybind11FilteredModel.referenceMap)

        val overloadsValidationResult =
            PythonOverloadsValidator(pythonNameResolver, signatureResolver, limeLogger, overloadsWerror)
                .validate(pythonFilteredModel.referenceMap.values)
        if (!overloadsValidationResult) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }
        val nameResolvers =
            mapOf(
                "" to pythonNameResolver,
                "Pybind11" to pybind11NameResolver,
                // The pybind11 trampoline is C++ code that must match the generated C++ base
                // signature exactly (including the `Return<T, Error>` wrapper for throwing
                // functions). Reusing the C++ name resolver lets the trampoline templates pull
                // in `cpp/CppReturnType.mustache`, which already emits that wrapper.
                "C++" to pybind11NameResolver,
            )
        // Only top-level enums are "standalone" (have their own Python module). Nested enums
        // are rendered inside their parent class/struct and use the simple integer-enum format.
        val standaloneEnumNames =
            pythonFilteredModel.topElements
                .filterIsInstance<LimeEnumeration>()
                .map { it.fullName }
                .toSet()
        val predicates =
            PythonGeneratorPredicates(
                limeOverloadsValidatorSignatureResolver(pybind11FilteredModel),
                pythonFilteredModel.referenceMap,
                pybind11FilteredModel.referenceMap,
                pybind11NameResolver,
                pythonNameResolver,
                standaloneEnumNames,
                internalNamespace,
            )

        val pybind11IncludeResolver = Pybind11IncludeResolver(pybind11FilteredModel.referenceMap, cppNameRules, internalNamespace)
        val pybind11IncludeCollector =
            GenericIncludesCollector(
                pybind11IncludeResolver,
                retainPredicate = { true },
            )

        val pythonFiles =
            pythonFilteredModel.topElements.flatMap {
                generatePythonFile(it, nameResolvers, predicates.predicates)
            }
        val pybind11Files =
            pybind11FilteredModel.topElements.flatMap {
                generatePybind11File(it, nameResolvers, pybind11IncludeCollector, predicates.predicates, pybind11FilteredModel)
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
        val imports =
            pythonImportsCollector.collectImports(limeElement)
                .filterNot { it.modulePath == selfModulePath }
                .distinct()
                .sorted()

        // Detect name clashes: two imports with the same importedName from different module
        // paths would shadow each other (the second `from a.b import X` overwrites the first
        // `from c.d import X`). For each clashed name, assign a deterministic alias derived
        // from the module path (dots → underscores) so both are accessible at runtime.
        val nameCounts = imports.filter { it.importedName != null }
            .groupingBy { it.importedName!! }
            .eachCount()
        val clashedNames = nameCounts.filter { it.value > 1 }.keys
        val clashAliases = mutableMapOf<String, String>()
        val importsWithAliases =
            if (clashedNames.isEmpty()) {
                imports
            } else {
                imports.map { imp ->
                    if (imp.importedName != null && imp.importedName in clashedNames) {
                        val alias = imp.modulePath.replace(".", "_")
                        clashAliases[imp.modulePath] = alias
                        imp.copy(alias = alias)
                    } else {
                        imp
                    }
                }
            }

        // Set the clash alias map so the name resolver substitutes aliases for clashed types
        // in type references (annotations, _wrap/_unwrap arguments, etc.).
        pythonNameResolver.setClashAliases(clashAliases)
        try {
            val contentBody = generateTypeBody(limeElement, nameResolvers, predicates, isStub = false)
            val stubBody = generateTypeBody(limeElement, nameResolvers, predicates, isStub = true)

            val templateData =
                mapOf(
                    "imports" to importsWithAliases,
                    "moduleName" to pythonModule,
                    "nativeModule" to pythonModule,
                    "usesCallable" to usesCallableForFile(limeElement),
                    "content" to contentBody,
                    "stubContent" to stubBody,
                )
            val content = TemplateEngine.render("python/PythonFile", templateData + ("isStub" to false), nameResolvers, predicates)
            val stubContent = TemplateEngine.render("python/PythonStub", templateData + ("isStub" to true), nameResolvers, predicates)
            return listOf(
                GeneratedFile(content, nameRules.getPythonFileName(limeElement)),
                GeneratedFile(stubContent, nameRules.getPythonStubFileName(limeElement)),
            )
        } finally {
            pythonNameResolver.clearClashAliases()
        }
    }

    /**
     * Recursively generates the Python class/struct/enum/etc. body for a LIME element, including
     * all nested types rendered as physically nested Python class definitions with proper
     * indentation. The result is a pre-rendered string injected into the file-level template
     * via `{{{content}}}` or `{{{stubContent}}}`.
     *
     * @param isStub if true, renders the type-stub (.pyi) template; otherwise the implementation (.py) template.
     */
    private fun generateTypeBody(
        element: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        predicates: Map<String, (Any) -> Boolean>,
        isStub: Boolean,
    ): String {
        // 1. Recursively generate nested type bodies and indent them.
        val nestedTypesStr = generateNestedTypeBodies(element, nameResolvers, predicates, isStub)

        // 2. Render THIS type's template.
        val templateName =
            (if (isStub) selectPythonStubTemplate(element) else selectPythonTemplate(element))
                ?: return ""
        // Set context so resolveValue can distinguish same-top-level vs cross-file
        // references when resolving constant values (e.g. StateEnum.ON vs RouteUtils.RouteType.EQUESTRIAN).
        pythonNameResolver.setContext(element)
        try {
        val templateData =
            mapOf(
                "model" to element,
                "nativeModule" to pythonModule,
                "typeName" to pythonNameResolver.resolvePybind11AccessPath(element),
                "nativeTypeName" to pythonNameResolver.resolvePybind11AccessPath(element),
                "nestedTypes" to nestedTypesStr,
                "isStub" to isStub,
            ) + (
                if (element is com.here.gluecodium.model.lime.LimeTypeAlias) {
                    mapOf("typeRefShortName" to pythonNameResolver.resolveShortTypeRef(element.typeRef, element))
                } else if (element is com.here.gluecodium.model.lime.LimeLambda) {
                    val fn = element.asFunction()
                    mapOf(
                        "typeRefShortName" to pythonNameResolver.resolveShortTypeRef(fn.returnType.typeRef, element),
                        "parameterTypes" to fn.parameters.joinToString(", ") {
                            pythonNameResolver.resolveShortTypeRef(it.typeRef, element)
                        },
                    )
                } else {
                    emptyMap()
                }
            )
        val result = TemplateEngine.render(templateName, templateData, nameResolvers, predicates)
        return result
        } finally {
            pythonNameResolver.clearContext()
        }
    }

    /**
     * Generates the nested type bodies for a container element, recursively rendering each nested
     * type and indenting the combined result by one Python indentation level (4 spaces). Returns
     * an empty string if the element has no nested types or is not a container.
     */
    private fun generateNestedTypeBodies(
        element: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        predicates: Map<String, (Any) -> Boolean>,
        isStub: Boolean,
    ): String {
        val container = element as? com.here.gluecodium.model.lime.LimeContainer ?: return ""
        // Reorder: structs, classes, interfaces, enumerations, and exceptions first,
        // then typeAliases and lambdas last. This ensures that types referenced by
        // type aliases and lambdas are already defined when the alias is evaluated
        // (avoiding forward-reference NameErrors at runtime inside the class body).
        val nestedTypes =
            container.structs + container.classes + container.interfaces +
                container.enumerations + container.exceptions +
                container.typeAliases + container.lambdas
        if (nestedTypes.isEmpty()) return ""

        val nestedBodies =
            nestedTypes
                .map { generateTypeBody(it, nameResolvers, predicates, isStub) }
                .filter { it.isNotBlank() }
        if (nestedBodies.isEmpty()) return ""

        return "\n" + nestedBodies.joinToString("\n\n").prependIndent("    ")
    }

    private fun generatePybind11File(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        includeCollector: GenericIncludesCollector,
        predicates: Map<String, (Any) -> Boolean>,
        pybind11FilteredModel: LimeModel,
    ): List<GeneratedFile> {
        val limeType = limeElement as? com.here.gluecodium.model.lime.LimeType ?: return emptyList()

        // Collect all types (top-level + nested) for this top-level element, excluding internal
        // types and types that emit no binding (type aliases, lambdas).
        val allTypes = collectPybind11Types(limeType, pybind11FilteredModel.referenceMap)
        if (allTypes.isEmpty()) return emptyList()

        // Collect includes for all types in the tree. Enum-based exceptions have no dedicated
        // header (they map to std::error_code); struct-backed exceptions need the payload header.
        val includes =
            allTypes
                .flatMap { type ->
                    if (type is com.here.gluecodium.model.lime.LimeException &&
                        type.errorType.type.actualType !is LimeStruct
                    ) {
                        emptyList()
                    } else {
                        includeCollector.collectImports(type)
                    }
                }.distinct().sorted()

        // Collect `using` aliases for all types (except exceptions, which have no C++ type).
        val aliases =
            allTypes.mapNotNull { type ->
                if (type is com.here.gluecodium.model.lime.LimeException) return@mapNotNull null
                val shortName = pybind11NameResolver.resolveName(type)
                val fullName = cppNameCache.getFullyQualifiedName(type)
                if (shortName != fullName) {
                    mapOf("shortName" to shortName, "fullName" to fullName)
                } else {
                    null
                }
            }

        // Render trampolines and binding bodies for each type.
        val trampolines = StringBuilder()
        val bindings = StringBuilder()

        for (type in allTypes) {
            val bindingTemplateName = selectPybind11Template(type) ?: continue

            // C++ variable name for the py::class_ object (used as scope for nested children).
            val varName = "cls_" + nameRules.getFlattenedName(type)
            // Scope: `module` for top-level types, parent's variable for nested types.
            val scope =
                if (type.path.hasParent) {
                    val parentPath = type.path.parent.toString()
                    val parent = pybind11FilteredModel.referenceMap[parentPath] as? LimeNamedElement
                    if (parent != null) "cls_" + nameRules.getFlattenedName(parent) else "module"
                } else {
                    "module"
                }
            // pybind11 registration name: flattened with package for top-level, short for nested.
            val pybindName = pythonNameResolver.resolvePybind11ShortName(type)

            // Render trampoline class (classes and interfaces only).
            val trampolineTemplateName = selectPybind11TrampolineTemplate(type)
            if (trampolineTemplateName != null) {
                val trampolineData = mapOf("model" to type)
                val trampolineResult =
                    TemplateEngine.render(trampolineTemplateName, trampolineData, nameResolvers, predicates)
                if (trampolineResult.isNotBlank()) {
                    trampolines.append(trampolineResult)
                    trampolines.append("\n")
                }
            }

            // Render binding body (py::class_ / py::enum_ / exception translator).
            val bindingData =
                mapOf(
                    "model" to type,
                    "scope" to scope,
                    "pybindName" to pybindName,
                    "varName" to varName,
                    "internalNamespaceStr" to internalNamespace.joinToString("::"),
                    "returnTypeFullName" to (internalNamespace + "Return").joinToString("::"),
                    "baseClasses" to
                        (type as? LimeContainerWithInheritance)
                            ?.parents
                            ?.mapNotNull { it.type.actualType as? LimeNamedElement }
                            ?.filter { pybind11FilteredModel.referenceMap.containsKey(it.fullName) }
                            ?.map { mapOf("fqn" to cppNameCache.getFullyQualifiedName(it)) }
                            .orEmpty(),
                    "pybind11AttrChain" to pythonNameResolver.resolvePybind11AttrChain(type),
                )
            bindings.append(TemplateEngine.render(bindingTemplateName, bindingData, nameResolvers, predicates))
            bindings.append("\n")
        }

        val templateData =
            mapOf(
                "includes" to includes,
                "aliases" to aliases,
                "trampolines" to trampolines.toString(),
                "bindings" to bindings.toString(),
                "registerName" to pythonNameResolver.resolveRegisterName(limeElement),
            )
        val content = TemplateEngine.render("python/Pybind11File", templateData, nameResolvers, predicates)
        return listOf(GeneratedFile(content, nameRules.getPybind11FileName(limeElement)))
    }

    /**
     * Recursively collects all types (top-level + nested) that should emit a pybind11 binding,
     * in parent-before-child order. Excludes type aliases and lambdas (which emit no binding).
     * Internal (@Internal) types are included — their Python-side names are underscore-prefixed
     * by PythonNameRules, but the pybind11 binding exposes them so the Python wrapper can access
     * the native C++ object.
     */
    private fun collectPybind11Types(
        limeType: LimeType,
        referenceMap: Map<String, LimeElement>,
    ): List<LimeType> {
        val result = mutableListOf<LimeType>()

        // Add this type (skip type aliases and lambdas — they emit no binding).
        if (limeType !is LimeTypeAlias && limeType !is com.here.gluecodium.model.lime.LimeLambda) {
            result.add(limeType)
        }

        // Recursively collect nested types.
        val container = limeType as? com.here.gluecodium.model.lime.LimeContainer ?: return result
        val nestedTypes =
            container.structs + container.classes + container.interfaces +
                container.enumerations + container.exceptions +
                container.typeAliases + container.lambdas
        for (nested in nestedTypes) {
            result.addAll(collectPybind11Types(nested, referenceMap))
        }
        return result
    }

    private fun selectPybind11TrampolineTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is com.here.gluecodium.model.lime.LimeClass -> "python/Pybind11ClassTrampoline"
            is com.here.gluecodium.model.lime.LimeInterface -> "python/Pybind11InterfaceTrampoline"
            else -> null
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
        // Wrapper cache: preserves referential equality across the C++ <-> Python boundary by
        // mapping a C++ instance pointer to a single Python wrapper object.
        val wrapperCacheContent =
            TemplateEngine.render("python/Pybind11WrapperCache", emptyMap<String, Any>(), nameResolvers, predicates)

        // Custom type caster for Gluecodium's Return<T, Error> adapter.
        val casterContent =
            TemplateEngine.render("python/Pybind11ReturnCaster", casterTemplateData, nameResolvers, predicates)

        // Module entry point: aggregates every per-top-level-element register_* function into a
        // single PYBIND11_MODULE. With Option B, one register_* function is emitted per top-level
        // LIME element (not per type), and it registers the top-level type AND all nested types
        // using nested py::class_ scopes. Type aliases and lambdas emit no binding.
        //
        // The register_* functions must be emitted in dependency order: a base class must be
        // registered before any derived class that lists it as a py::class_ base (pybind11 looks
        // up the base type info at construction time and throws if it is not yet registered).
        // Since nested types are registered within their parent's register function, the
        // dependency graph operates at the top-level register-function level: if any type in
        // top-level element T's tree inherits from any type in top-level element S's tree, then
        // register_S must be called before register_T.
        val topLevelBoundTypes =
            pybind11FilteredModel.topElements
                .filterIsInstance<LimeType>()
                .filter { it !is LimeTypeAlias && it !is com.here.gluecodium.model.lime.LimeLambda }
        // For each top-level type, find all top-level register names it depends on.
        val registerNameToDeps =
            topLevelBoundTypes.associate { topType ->
                val topRegName = pythonNameResolver.resolveRegisterName(topType)
                val allTypesInTree = collectPybind11Types(topType, pybind11FilteredModel.referenceMap)
                val deps =
                    allTypesInTree
                        .mapNotNull { it as? LimeContainerWithInheritance }
                        .flatMap { container ->
                            container.parents
                                .mapNotNull { it.type.actualType as? LimeNamedElement }
                                .filter { pybind11FilteredModel.referenceMap.containsKey(it.fullName) }
                                .map { pythonNameResolver.resolveTopLevelRegisterName(it) }
                        }
                        .filter { it != topRegName }
                        .distinct()
                topRegName to deps
            }
        val registerFunctions =
            topologicalSort(registerNameToDeps).map { mapOf("name" to it) }
        val moduleInitTemplateData =
            mapOf(
                "moduleName" to pythonModule,
                "moduleDoc" to "Generated Python bindings for the '$pythonModule' extension module.",
                "registerFunctions" to registerFunctions,
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
            GeneratedFile(
                TemplateEngine.render("python/Pybind11GenericCaster", emptyMap<String, Any>(), nameResolvers, predicates),
                PythonNameRules.PYBIND11_TARGET_DIRECTORY + "_generic_caster.h",
            ),
            GeneratedFile(moduleInitContent, PythonNameRules.MODULE_INIT_FILE),
            GeneratedFile(setupPyContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "setup.py"),
            GeneratedFile(pyprojectContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "pyproject.toml"),
            GeneratedFile(nativeBaseContent, PythonNameRules.PYTHON_TARGET_DIRECTORY + "_native_base.py"),
        ) + packageInitFiles
    }

    // Topologically sorts type names so that every base class appears before its derived
    // classes. `parents` maps each type name to the names of its (bound) base classes. A stable
    // sort is used for ties so the output stays deterministic. Cycles are not expected (LIME
    // forbids them), but if one occurs the remaining nodes are appended in input order rather
    // than looping forever.
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
                            it is com.here.gluecodium.model.lime.LimeException ||
                            it is com.here.gluecodium.model.lime.LimeLambda
                    }.filter { it != topType }
        }.distinctBy { it.fullName }

    /**
     * Checks whether any type in the element's type tree (including nested types) uses a
     * Callable/lambda type, so the file-level `from typing import Callable` import can be
     * emitted when needed.
     */
    private fun usesCallableForFile(limeElement: LimeNamedElement): Boolean =
        LimeTypeHelper.getAllTypes(limeElement).any { usesCallable(it) }

    private fun usesCallable(limeElement: LimeNamedElement): Boolean =
        when (limeElement) {
            is LimeLambda -> true
            is LimeTypeAlias -> containsLambda(limeElement.typeRef)
            is LimeStruct ->
                limeElement.fields.any { containsLambda(it.typeRef) } ||
                    limeElement.functions.any { function ->
                        function.parameters.any { containsLambda(it.typeRef) } || containsLambda(function.returnType.typeRef)
                    } ||
                    limeElement.properties.any { containsLambda(it.typeRef) }
            is com.here.gluecodium.model.lime.LimeContainer ->
                limeElement.functions.any { function ->
                    function.parameters.any { containsLambda(it.typeRef) } || containsLambda(function.returnType.typeRef)
                } || limeElement.properties.any { containsLambda(it.typeRef) }
            else -> false
        }

    private fun containsLambda(limeTypeRef: LimeTypeRef): Boolean =
        when (val limeType = limeTypeRef.type) {
            is LimeTypeAlias -> containsLambda(limeType.typeRef)
            is LimeGenericType -> limeType.childTypes.any(::containsLambda)
            else -> limeType.actualType is LimeLambda
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

    private fun selectPythonStubTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is com.here.gluecodium.model.lime.LimeTypeAlias -> "python/PythonStubTypeAlias"
            is com.here.gluecodium.model.lime.LimeException -> "python/PythonStubException"
            is com.here.gluecodium.model.lime.LimeLambda -> "python/PythonStubLambda"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "python/PythonStubEnumeration"
            is com.here.gluecodium.model.lime.LimeStruct -> "python/PythonStubStruct"
            is com.here.gluecodium.model.lime.LimeClass -> "python/PythonStubClass"
            is com.here.gluecodium.model.lime.LimeInterface -> "python/PythonStubInterface"
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
