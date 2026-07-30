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

import com.here.gluecodium.generator.common.CommonGeneratorPredicates
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeAttributeValueType.REF
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSignatureResolver
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeRef

/**
 * List of predicates used by `ifPredicate`/`unlessPredicate` template helpers in the Python generator.
 */
internal class PythonGeneratorPredicates(
    private val signatureResolver: LimeSignatureResolver,
    private val limeReferenceMap: Map<String, LimeElement>,
    // The pybind11-filtered reference map (retains @Internal elements). Used by
    // `isNestedInternal` so it can walk up the parent chain even when an internal
    // ancestor has been filtered out of the python-filtered `limeReferenceMap`.
    private val pybind11ReferenceMap: Map<String, LimeElement>,
    private val pybind11NameResolver: Pybind11NameResolver,
    private val pythonNameResolver: PythonNameResolver,
    private val standaloneEnums: Set<String>,
    private val internalNamespace: List<String>,
) {
    // Collects all functions visible on a container, including those inherited from parent
    // containers (interfaces/classes). In C++ a child class exposes every inherited overload, so
    // this is what determines whether a method pointer is ambiguous for pybind11's .def().
    private fun allContainerFunctions(
        container: com.here.gluecodium.model.lime.LimeContainer,
    ): List<com.here.gluecodium.model.lime.LimeFunction> {
        val own = container.functions
        val inherited =
            (container as? com.here.gluecodium.model.lime.LimeContainerWithInheritance)
                ?.parents
                .orEmpty()
                .mapNotNull { it.type.actualType as? com.here.gluecodium.model.lime.LimeContainer }
                .flatMap { allContainerFunctions(it) }
        return own + inherited
    }

    // Returns true if `descendant` inherits (directly or transitively) from `ancestor`.
    private fun isDescendantOf(
        descendant: com.here.gluecodium.model.lime.LimeContainerWithInheritance,
        ancestor: com.here.gluecodium.model.lime.LimeContainer,
    ): Boolean {
        val visited = mutableSetOf<String>()
        val queue = ArrayDeque<com.here.gluecodium.model.lime.LimeContainerWithInheritance>().apply { add(descendant) }
        while (queue.isNotEmpty()) {
            val current = queue.removeFirst()
            if (current.path.toString() == ancestor.path.toString()) return true
            if (!visited.add(current.path.toString())) continue
            current.parents
                .mapNotNull { it.type.actualType as? com.here.gluecodium.model.lime.LimeContainerWithInheritance }
                .forEach { queue.add(it) }
        }
        return false
    }

    val predicates =
        mapOf(
            "hasAnyComment" to { limeElement: Any ->
                CommonGeneratorPredicates.hasAnyComment(limeElement, "Python")
            },
            "isInterface" to { it is com.here.gluecodium.model.lime.LimeInterface },
            // Whether the container needs a pybind11 trampoline class so it can be subclassed from
            // Python. Mirrors Pybind11Helpers.needsTrampoline: interfaces always need one, and a
            // class needs one when it is open or inherits from another container (so inherited
            // pure-virtual methods are overridden and the trampoline is instantiable).
            "needsTrampoline" to { limeElement: Any ->
                when (limeElement) {
                    is com.here.gluecodium.model.lime.LimeInterface -> true
                    is com.here.gluecodium.model.lime.LimeClass ->
                        limeElement.isOpen || limeElement.parents.isNotEmpty()
                    else -> false
                }
            },
            // Whether the container has more than one base class (true multiple inheritance). When
            // set, the pybind11 `py::class_` must be constructed with `py::multiple_inheritance()`
            // so pybind11 uses dynamic_cast-based safe casting instead of assuming a zero pointer
            // offset for the second and later base classes. Without it, direct member access
            // (property getters/setters) on a non-first base silently reads/writes the wrong memory
            // offset, while virtual dispatch via the vtable still happens to work.
            "needsMultipleInheritanceTag" to { limeElement: Any ->
                (limeElement as? com.here.gluecodium.model.lime.LimeContainerWithInheritance)
                    ?.parents
                    ?.size
                    ?.let { it > 1 } == true
            },
            "isInternal" to { it is LimeNamedElement && CommonGeneratorPredicates.isInternal(it, PYTHON) },
            "isPublic" to { it is LimeNamedElement && !CommonGeneratorPredicates.isInternal(it, PYTHON) },
            // Whether a function/property/field is skipped for Python and must not get an actual
            // pybind11 binding (`.def()` / `.def_property()` / `.def_readwrite()`), even though it
            // is still present in the model this class was built from (`pybind11FilteredModel`,
            // built with `retainFunctionsAndFields = true`). That flag exists so container bodies
            // stay complete for the C++-facing trampoline (an interface's Python trampoline must
            // override *every* pure-virtual member, including Python-skipped ones, to remain a
            // valid concrete C++ type) - it must not also cause skipped members to be exposed to
            // Python users. `limeReferenceMap` here is `pythonFilteredModel.referenceMap`, i.e. the
            // strict model built with `retainFunctionsAndFields = false`, which is exactly the
            // membership test we need: present there means "not skipped for Python".
            "isSkippedForPython" to { limeElement: Any ->
                limeElement is LimeNamedElement && !limeReferenceMap.containsKey(limeElement.fullName)
            },
            "isNestedInternal" to { limeElement: Any ->
                limeElement is LimeNamedElement &&
                    generateSequence(limeElement) {
                        pybind11ReferenceMap[it.path.parent.toString()] as? LimeNamedElement
                    }.any { CommonGeneratorPredicates.isInternal(it, PYTHON) }
            },
            "isStandaloneEnum" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeEnumeration &&
                    limeElement.fullName in standaloneEnums
            },
            // Whether a struct (or class) has the @Equatable attribute. When true,
            // PythonStruct.mustache emits __eq__ and __hash__ methods that delegate
            // to the C++ operator== and std::hash via the native pybind11 object.
            "isEquatable" to { limeElement: Any ->
                limeElement is LimeNamedElement &&
                    limeElement.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.EQUATABLE)
            },
            "isOverloaded" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    signatureResolver.isOverloaded(limeFunction)
            },
            // Whether this function is the FIRST one (in declaration order) among the container's
            // own functions that resolves to the same Python name. The Python wrapper layer can only
            // hold a single method per name, so exactly one representative is emitted (a generic
            // *args/**kwargs dispatcher) and the rest are skipped. This predicate is evaluated with
            // the function as context, but it needs the enclosing container to find siblings, so it
            // walks up via the function's path parent.
            "isFirstOverload" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    run {
                        val container =
                            limeReferenceMap[limeFunction.path.parent.toString()]
                                as? com.here.gluecodium.model.lime.LimeContainer ?: return@run false
                        val pythonName = pythonNameResolver.resolveName(limeFunction)
                        container.functions.indexOfFirst { pythonNameResolver.resolveName(it) == pythonName } ==
                            container.functions.indexOf(limeFunction)
                    }
            },
            // Whether the C++ name of this function collides with another function in the same
            // container OR an inherited one. In C++ a child class exposes all inherited overloads,
            // so pybind11 needs py::overload_cast whenever the resolved C++ name appears more than
            // once across the full inheritance hierarchy (e.g. foo() inherited + foo(String) own).
            "isCppOverloaded" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    run {
                        val declaringContainer =
                            limeReferenceMap[limeFunction.path.parent.toString()]
                                as? com.here.gluecodium.model.lime.LimeContainer ?: return@run false
                        val cppName = pybind11NameResolver.resolveName(limeFunction)
                        // Containers where this function is visible: the declaring container itself
                        // plus every descendant that inherits from it (directly or transitively).
                        val visibleContainers =
                            sequence {
                                yield(declaringContainer)
                                limeReferenceMap.values
                                    .filterIsInstance<com.here.gluecodium.model.lime.LimeContainerWithInheritance>()
                                    .filter { it != declaringContainer && isDescendantOf(it, declaringContainer) }
                                    .forEach { yield(it) }
                            }
                        visibleContainers.any { container ->
                            allContainerFunctions(container).count { pybind11NameResolver.resolveName(it) == cppName } > 1
                        }
                    }
            },
            "needsInterfaceLambdaBinding" to { limeElement: Any ->
                val isStatic =
                    when (limeElement) {
                        is com.here.gluecodium.model.lime.LimeFunction -> limeElement.isStatic
                        is com.here.gluecodium.model.lime.LimeProperty -> limeElement.isStatic
                        else -> true
                    }
                !isStatic &&
                    when (limeElement) {
                        is com.here.gluecodium.model.lime.LimeFunction ->
                            limeReferenceMap[limeElement.path.parent.toString()]
                        is com.here.gluecodium.model.lime.LimeProperty ->
                            limeReferenceMap[limeElement.path.parent.toString()]
                        else -> null
                    } is com.here.gluecodium.model.lime.LimeInterface
            },
            // Whether a type reference refers to a user-defined (generated-wrapper) type that must be
            // unwrapped to its native `_native` handle before being passed to a pybind11 call.
            "isWrapperType" to { limeTypeRef: Any ->
                limeTypeRef is LimeTypeRef &&
                    limeTypeRef.type.actualType.let {
                        it !is com.here.gluecodium.model.lime.LimeBasicType &&
                            it !is com.here.gluecodium.model.lime.LimeGenericType &&
                            it !is LimeLambda
                    }
            },
            "isLambdaType" to { limeTypeRef: Any ->
                limeTypeRef is LimeTypeRef && limeTypeRef.type.actualType is LimeLambda
            },
            "isCollectionType" to { limeTypeRef: Any ->
                limeTypeRef is LimeTypeRef && isCollectionType(limeTypeRef.type)
            },
            "needsLambdaBinding" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    (
                        limeFunction.parameters.any { it.typeRef.type.actualType is LimeLambda } ||
                            limeFunction.returnType.typeRef.type.actualType is LimeLambda
                    )
            },
            "needsCollectionLambdaBinding" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    (
                        limeFunction.parameters.any { it.typeRef.type.actualType is LimeLambda } ||
                            limeFunction.returnType.typeRef.type.actualType is LimeLambda ||
                            limeFunction.parameters.any { isCollectionType(it.typeRef.type) } ||
                            isCollectionType(limeFunction.returnType.typeRef.type)
                    )
            },
            // pybind11 must see a literal std::function signature for direct lambda parameters
            // and returns. Collection parameters need the same wrapper so the generic caster can
            // recursively convert their elements.
            "needsCallableBinding" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    (
                        limeFunction.parameters.any { it.typeRef.type.actualType is LimeLambda } ||
                            limeFunction.returnType.typeRef.type.actualType is LimeLambda ||
                            limeFunction.parameters.any { isCollectionType(it.typeRef.type) } ||
                            isCollectionType(limeFunction.returnType.typeRef.type)
                    )
            },
            "needsAllFieldsConstructor" to { limeStruct: Any ->
                when {
                    limeStruct !is LimeStruct -> false
                    limeStruct.fieldConstructors.isEmpty() -> true
                    limeStruct.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) ->
                        limeStruct.allFieldsConstructor == null
                    else -> false
                }
            },
            // Whether the C++ representation of a type reference needs a '&' suffix when used as a
            // function parameter (mirrors the C++ generator's needsRefSuffix predicate). Used by the
            // pybind11 trampoline so its override signatures match the base class exactly.
            "needsRefSuffix" to { limeTypeRef: Any ->
                limeTypeRef is LimeTypeRef && CppNameResolver.needsRefSuffix(limeTypeRef)
            },
            // Whether a property has a setter. Used (instead of a `{{#setter}}` section) so the
            // template context (`this`) stays the property and `resolveSetterName` receives the
            // property rather than the setter function.
            "hasSetter" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeProperty && limeElement.setter != null
            },
            "hasFieldAccessors" to { limeElement: Any ->
                limeElement is LimeField && pybind11NameResolver.resolveGetterName(limeElement) != null
            },
            "hasCppRef" to { limeElement: Any ->
                limeElement is LimeProperty && limeElement.attributes.have(CPP, REF)
            },
            // Whether a function/property carries `@Cpp(Const)`. The generated C++ declares such
            // methods as `const`, so the pybind11 trampoline override must also be `const` to
            // match the virtual signature (otherwise it "hides" the base method and the trampoline
            // class stays abstract, failing to instantiate).
            "isCppConst" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeFunction &&
                    limeElement.attributes.have(CPP, com.here.gluecodium.model.lime.LimeAttributeValueType.CONST)
            },
            // Whether a function/property carries `@Cpp(Noexcept)`. The generated C++ declares such
            // methods as `noexcept`, so the pybind11 trampoline override must also be `noexcept`
            // to match the virtual signature (otherwise "exception specification ... more lax than base
            // version" and the trampoline class stays abstract).
            "isCppNoexcept" to { limeElement: Any ->
                val limeNamed =
                    limeElement as? com.here.gluecodium.model.lime.LimeFunction
                        ?: limeElement as? com.here.gluecodium.model.lime.LimeProperty
                limeNamed?.attributes?.have(
                    CPP,
                    com.here.gluecodium.model.lime.LimeAttributeValueType.NOEXCEPT,
                ) == true
            },
            "isImmutableField" to { limeElement: Any ->
                limeElement is LimeField &&
                    run {
                        val parentKey = limeElement.path.parent.toString()
                        val parent = limeReferenceMap[parentKey] as? LimeStruct
                        val parentIsImmutable = parent?.attributes?.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) == true
                        val fieldType = limeElement.typeRef.type.actualType
                        val fieldTypeIsImmutable = fieldTypeHasImmutableFields(fieldType)
                        parentIsImmutable || fieldTypeIsImmutable
                    }
            },
            // Whether a field's type is one of the *ancestors* of its own container (e.g. a
            // nested struct with a field pointing back to its enclosing class, as in
            // `InstanceInStruct.SelfHolder.mySelf: InstanceInStruct`). Nested types are
            // flattened into separate top-level Python modules, so such a field would otherwise
            // require a module-level `from ...InstanceInStruct import InstanceInStruct` while
            // `InstanceInStruct`'s own module needs `from ...SelfHolder import SelfHolder` for
            // its factory return types - an unresolvable circular import. `PythonField` uses
            // this predicate to emit a local (deferred) import instead of a module-level one.
            "isAncestorField" to { limeElement: Any -> limeElement is LimeField && isFieldTypeAncestor(limeElement) },
            // Whether a function's return type creates a circular import with its own container.
            // This happens in two patterns:
            // 1. The return type is an *ancestor* of the container (e.g. a nested class
            //    `Builder.build()` returning its enclosing struct `OuterStruct`).
            // 2. The return type is a *descendant* of the container (e.g.
            //    `InstanceInStruct.createInStruct()` returning the nested struct `SelfHolder`).
            // In both cases, nested types are flattened into separate top-level Python modules
            // that would import each other at module level — an unresolvable circular import.
            // `PythonFunction.mustache` uses this predicate to emit a local (deferred) import
            // inside the method body instead.
            "isAncestorReturnType" to { limeElement: Any ->
                val func = limeElement as? com.here.gluecodium.model.lime.LimeFunction
                func != null && isCircularTypeRef(func, func.returnType.typeRef)
            },
            // Whether a property's type creates a circular import with its own container.
            // Mirrors `isAncestorField` / `isAncestorReturnType` but for property types.
            "isAncestorProperty" to { limeElement: Any ->
                val prop = limeElement as? com.here.gluecodium.model.lime.LimeProperty
                prop != null && isCircularTypeRef(prop, prop.typeRef)
            },
            // Whether the element lives inside a non-empty namespace (i.e. its LimePath head is not
            // empty). Used by the pybind11 file template to emit `using` aliases so the generated
            // code can refer to the C++ type by its short name.
            "hasNamespace" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeClass ||
                    limeElement is com.here.gluecodium.model.lime.LimeStruct ||
                    limeElement is com.here.gluecodium.model.lime.LimeInterface ||
                    limeElement is com.here.gluecodium.model.lime.LimeEnumeration
            },
            // Whether the element is a LimeException. Exceptions are represented as `std::error_code`
            // in C++ (no dedicated type/header), so the pybind11 file template skips the `using`
            // alias for them.
            "isException" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeException
            },
            // Whether an exception's error type is an enum (LimeEnumeration). Enum-based errors
            // map to std::error_code in C++, and the thrown exception type is std::system_error.
            // Struct-based errors map to the struct type itself, which is thrown directly.
            "isEnumError" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeException &&
                    limeElement.errorType.type.actualType is com.here.gluecodium.model.lime.LimeEnumeration
            },
            // Whether a function/constructor throws (has a non-null exception type). Throwing
            // functions are bound in the pybind11 layer; the Return<T, Error> type caster
            // translates errors into the specific Python exception registered by
            // Pybind11Exception.mustache.
            "isThrowing" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeFunction &&
                    limeElement.exception != null
            },
            // Whether the C++ return type of a function contains a comma (e.g. a `std::map<K, V>` or
            // `std::pair<A, B>` instantiation). The `PYBIND11_OVERRIDE_PURE` / `PYBIND11_OVERRIDE`
            // Whether a function/property's (unwrapped) return type is `void`. Used by the
            // forwarding trampoline to decide whether an override forwards a value or not.
            "isVoid" to { limeElement: Any ->
                val typeRef =
                    when (limeElement) {
                        is com.here.gluecodium.model.lime.LimeFunction -> limeElement.returnType.typeRef
                        is com.here.gluecodium.model.lime.LimeProperty -> limeElement.typeRef
                        else -> null
                    }
                typeRef?.type?.actualType is com.here.gluecodium.model.lime.LimeBasicType &&
                    (typeRef.type.actualType as com.here.gluecodium.model.lime.LimeBasicType)
                        .typeId == com.here.gluecodium.model.lime.LimeBasicType.TypeId.VOID
            },
            // Whether the C++ signature of a function/property is `void`. Unlike `isVoid` (which
            // only looks at the unwrapped LIME return type), this also accounts for a thrown error
            // type: an error-returning function whose LIME return type is `void` still maps to a
            // non-void C++ signature (`std::error_code`), so the forwarding trampoline must return
            // the result of `m_impl->...` rather than discarding it.
            "isCppVoid" to { limeElement: Any ->
                val (typeRef, thrownType) =
                    when (limeElement) {
                        is com.here.gluecodium.model.lime.LimeFunction ->
                            limeElement.returnType.typeRef to limeElement.thrownType
                        is com.here.gluecodium.model.lime.LimeProperty -> limeElement.typeRef to null
                        else -> null to null
                    }
                thrownType == null &&
                    typeRef?.type?.actualType is com.here.gluecodium.model.lime.LimeBasicType &&
                    (typeRef.type.actualType as com.here.gluecodium.model.lime.LimeBasicType)
                        .typeId == com.here.gluecodium.model.lime.LimeBasicType.TypeId.VOID
            },
            // macros are not variadic in their type argument, so a comma-bearing return type must be
            // aliased through a `using` declaration before being passed to the macro. Accepts either
            // the function itself or its return type reference as the predicate context.
            "returnTypeHasComma" to { limeElement: Any ->
                val (typeRef, thrownType) =
                    when (limeElement) {
                        is com.here.gluecodium.model.lime.LimeFunction ->
                            limeElement.returnType.typeRef to limeElement.thrownType
                        is com.here.gluecodium.model.lime.LimeTypeRef -> limeElement to null
                        is com.here.gluecodium.model.lime.LimeProperty ->
                            limeElement.typeRef to null
                        else -> null to null
                    }
                // A throwing function's C++ return type is wrapped as
                // `Return<T, Error>` (or `Return<void, Error>` when T is void), which always contains
                // a comma, so the trampoline must alias it through a `using` declaration before the
                // PYBIND11_OVERRIDE_PURE macro. The unwrapped type is also checked for completeness.
                val wrappedHasComma = thrownType != null
                typeRef != null &&
                    (wrappedHasComma || pybind11NameResolver.resolveName(typeRef).contains(','))
            },
            // Whether a struct needs a `py::init<>()` with no arguments. Mirrors the C++ generator's
            // `hasDefaultConstructor` predicate: the C++ struct is default-constructible unless it is
            // immutable, has an explicit no-arg field constructor, or has an uninitialized field
            // whose (struct-recursively expanded) type is immutable. An explicit no-arg field constructor
            // already yields the same `py::init<>()`, so it is suppressed here to avoid registering a
            // duplicate constructor in pybind11.
            // IMPORTANT: unlike CommonGeneratorPredicates.getAllFieldTypes, this uses a local version that
            // does NOT unwrap through LimeTypeAlias/LimeList/LimeSet/LimeMap — only LimeStruct types are
            // descended into. This matches CppGeneratorPredicates.getAllFieldTypes and the C++
            // hasDefaultConstructor semantics (e.g. `List<SomeImmutableStruct>` IS default-constructible
            // because std::vector has a default constructor, even though some elements are immutable).
            "hasDefaultConstructor" to { limeElement: Any ->
                when {
                    limeElement !is com.here.gluecodium.model.lime.LimeStruct -> false
                    limeElement.fieldConstructors.any { it.fieldRefs.isEmpty() } -> false
                    limeElement.uninitializedFields.isEmpty() -> true
                    limeElement.uninitializedFields
                        .flatMap { pythonGetAllFieldTypes(it.typeRef.type) }
                        .any { it.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) } -> false
                    !limeElement.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) -> true
                    else -> false
                }
            },
            // Whether a struct has some fields with Lime defaults and some without, and no
            // explicit field constructor. Mirrors the C++ generator's `hasPartialDefaults`
            // predicate. When true, the pybind11 binding needs a constructor that takes only
            // the uninitialized fields, letting C++ default-initialize the rest.
            "hasPartialDefaults" to { limeElement: Any ->
                when {
                    limeElement !is com.here.gluecodium.model.lime.LimeStruct -> false
                    limeElement.uninitializedFields.isEmpty() -> false
                    limeElement.fieldConstructors.isNotEmpty() -> false
                    else -> limeElement.uninitializedFields.size < limeElement.fields.size
                }
            },
            // Whether a struct has any @Internal fields (regardless of default value).
            // Used by the struct init template to decide whether to use a lambda-based
            // constructor for the all-fields case.
            "hasInternalFields" to { limeElement: Any ->
                limeElement is LimeStruct &&
                    limeElement.fields.any { CommonGeneratorPredicates.isInternal(it, PYTHON) }
            },
            // Whether a struct has any @Internal fields that are also uninitialized (no default
            // value). When true, the pybind11 struct init template must use a lambda-based
            // constructor that default-constructs those internal fields instead of exposing
            // them as constructor parameters.
            "hasInternalUninitializedFields" to { limeElement: Any ->
                limeElement is LimeStruct &&
                    limeElement.uninitializedFields.any { CommonGeneratorPredicates.isInternal(it, PYTHON) }
            },
            // Whether a struct needs a `py::init<...>()` taking every field. True when the struct
            // has no explicit field constructors (so the implicit all-fields constructor is the
            // only one) or, for immutable structs, when no all-fields field constructor is declared.
            "needsAllFieldsConstructor" to { limeElement: Any ->
                when {
                    limeElement !is com.here.gluecodium.model.lime.LimeStruct -> false
                    limeElement.fields.isEmpty() -> false
                    limeElement.fieldConstructors.isEmpty() -> true
                    com.here.gluecodium.generator.common.CommonGeneratorPredicates
                        .hasImmutableFields(limeElement) -> limeElement.allFieldsConstructor == null
                    else -> false
                }
            },
            // Whether a field constructor takes no arguments (i.e. its fieldRefs list is empty).
            // Such a constructor must be bound as a plain `py::init<>()` rather than one carrying a
            // dangling empty `py::arg(...)`.
            "isEmptyFieldConstructor" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeFieldConstructor &&
                    limeElement.fieldRefs.isEmpty()
            },
        )

    private fun isFieldTypeAncestor(limeField: LimeField): Boolean {
        val fieldTypeName = (limeField.typeRef.type.actualType as? LimeNamedElement)?.fullName ?: return false
        return limeField.path.parent.allParents.any {
            limeReferenceMap[it.toString()]?.let {
                    e ->
                (e as? LimeNamedElement)?.fullName
            } == fieldTypeName
        }
    }

    private fun isCircularTypeRef(
        element: LimeNamedElement,
        typeRef: LimeTypeRef,
    ): Boolean {
        val referencedType = typeRef.type.actualType as? LimeNamedElement ?: return false
        val container = limeReferenceMap[element.path.parent.toString()] as? LimeNamedElement ?: return false
        // A circular import arises when the referenced type is a descendant of the element's
        // container (e.g. InstanceInStruct.createInStruct() -> SelfHolder, where SelfHolder
        // is a nested struct of InstanceInStruct). This is only a circular import when the
        // descendant type has a member that references an ancestor (e.g. SelfHolder has a
        // field `mySelf: InstanceInStruct`). Without such a back-reference, the descendant's
        // module does not import the container's module, so there is no cycle.
        //
        // The reverse direction (return type is an ANCESTOR of the container, e.g.
        // Builder.build() -> OuterStruct) does NOT need a deferred import here: the
        // `childModulePaths` mechanism in PythonGenerator.kt already detects when a child
        // module imports the parent and removes the parent's module-level import of the
        // child, breaking the cycle. The child can then safely import the parent at module
        // level because the parent no longer imports the child at module level.
        return isAncestorOf(container, referencedType) && hasAncestorReference(referencedType)
    }

    // Checks whether `descendant` has any member (field or property) whose type is an
    // ancestor of `descendant` itself. This is a proxy for "the descendant's module imports
    // the container's module", which is what creates the circular import in the DESCENDANT
    // direction.
    private fun hasAncestorReference(descendant: LimeNamedElement): Boolean {
        return when (descendant) {
            is LimeStruct ->
                descendant.fields.any { field ->
                    val fieldType = field.typeRef.type.actualType as? LimeNamedElement
                    fieldType != null && isAncestorOf(fieldType, descendant)
                }
            is com.here.gluecodium.model.lime.LimeContainerWithInheritance ->
                descendant.properties.any { prop ->
                    val propType = prop.typeRef.type.actualType as? LimeNamedElement
                    propType != null && isAncestorOf(propType, descendant)
                }
            else -> false
        }
    }

    private fun isAncestorOf(
        ancestor: LimeNamedElement,
        descendant: LimeNamedElement,
    ): Boolean {
        // Walk up from the descendant's path to find any ancestor matching the referenced type.
        // Use `tailParents` (which terminates once the tail is exhausted) instead of a manual
        // `parent` walk: `LimePath.parent` is idempotent for an empty tail, so a hand-rolled
        // `while (currentKey != null)` loop would never terminate when no ancestor matches,
        // causing the generator to spin indefinitely on deeply nested types.
        return descendant.path.tailParents.any {
            (limeReferenceMap[it.toString()] as? LimeNamedElement)?.fullName == ancestor.fullName
        }
    }

    private fun fieldTypeHasImmutableFields(limeType: LimeType): Boolean {
        return when (limeType) {
            is com.here.gluecodium.model.lime.LimeStruct ->
                com.here.gluecodium.generator.common.CommonGeneratorPredicates.hasImmutableFields(limeType)
            is com.here.gluecodium.model.lime.LimeTypeAlias ->
                fieldTypeHasImmutableFields(limeType.typeRef.type)
            is com.here.gluecodium.model.lime.LimeList ->
                fieldTypeHasImmutableFields(limeType.elementType.type)
            is com.here.gluecodium.model.lime.LimeSet ->
                fieldTypeHasImmutableFields(limeType.elementType.type)
            is com.here.gluecodium.model.lime.LimeMap ->
                fieldTypeHasImmutableFields(limeType.keyType.type) ||
                    fieldTypeHasImmutableFields(limeType.valueType.type)
            else -> false
        }
    }

    // Matches C++ `CppGeneratorPredicates.getAllFieldTypes`: only descends into LimeStruct
    // types, does NOT unwrap through LimeTypeAlias, LimeList, LimeSet, or LimeMap.
    // This is used by `hasDefaultConstructor` so that collection/alias-wrapped immutable
    // types are not incorrectly treated as making a struct non-default-constructible.
    private fun pythonGetAllFieldTypes(limeType: LimeType): List<LimeType> = pythonGetAllFieldTypesRec(limeType.actualType, mutableSetOf())

    private fun pythonGetAllFieldTypesRec(
        leafType: LimeType,
        visitedTypes: MutableSet<LimeType>,
    ): List<LimeType> {
        if (leafType !is LimeStruct) return listOf(leafType)
        visitedTypes += leafType
        val typesToVisit = leafType.fields.map { it.typeRef.type.actualType }.distinct() - visitedTypes
        return typesToVisit.flatMap { pythonGetAllFieldTypesRec(it, visitedTypes) } + leafType
    }

    private fun isCollectionType(limeType: LimeType): Boolean =
        when (limeType) {
            is com.here.gluecodium.model.lime.LimeList,
            is com.here.gluecodium.model.lime.LimeMap,
            is com.here.gluecodium.model.lime.LimeSet,
            -> true
            is com.here.gluecodium.model.lime.LimeTypeAlias -> isCollectionType(limeType.typeRef.type)
            else -> false
        }
}
