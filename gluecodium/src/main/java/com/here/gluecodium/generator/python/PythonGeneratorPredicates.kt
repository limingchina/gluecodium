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
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeValueType.REF
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeField
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
    private val pybind11NameResolver: Pybind11NameResolver,
    private val standaloneEnums: Set<String>,
) {
    val predicates =
        mapOf(
            "hasAnyComment" to { limeElement: Any ->
                CommonGeneratorPredicates.hasAnyComment(limeElement, "Python")
            },
            "isInterface" to { it is com.here.gluecodium.model.lime.LimeInterface },
            "isInternal" to { it is LimeNamedElement && CommonGeneratorPredicates.isInternal(it, PYTHON) },
            "isPublic" to { it is LimeNamedElement && !CommonGeneratorPredicates.isInternal(it, PYTHON) },
            "isNestedInternal" to { limeElement: Any ->
                limeElement is LimeNamedElement &&
                    generateSequence(limeElement) {
                        limeReferenceMap[it.path.parent.toString()] as? LimeNamedElement
                    }.any { CommonGeneratorPredicates.isInternal(it, PYTHON) }
            },
                    "isStandaloneEnum" to { limeElement: Any ->
                    limeElement is com.here.gluecodium.model.lime.LimeEnumeration &&
                        limeElement.fullName in standaloneEnums
                    },
            "isOverloaded" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    signatureResolver.isOverloaded(limeFunction)
            },
            // Whether the C++ name of this function collides with another function in the same
            // container (e.g. two Lime methods with different names that both map to the same C++
            // name via @Cpp). pybind11 requires py::overload_cast for such cases.
            "isCppOverloaded" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    run {
                        val container =
                            limeReferenceMap[limeFunction.path.parent.toString()]
                                as? com.here.gluecodium.model.lime.LimeContainer ?: return@run false
                        val cppName = pybind11NameResolver.resolveName(limeFunction)
                        container.functions.count { pybind11NameResolver.resolveName(it) == cppName } > 1
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
                            it !is com.here.gluecodium.model.lime.LimeGenericType
                    }
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
                limeElement is LimeField && run {
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
            // Whether a function's return type is one of the *ancestors* of its own container
            // (e.g. a nested class `Builder.build()` returning its enclosing struct `OuterStruct`).
            // Mirrors `isAncestorField` but for method/function return types, which produce the
            // same circular-import problem once nested types are flattened into top-level modules.
            "isAncestorReturnType" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeFunction && isTypeAncestor(limeElement.returnType.typeRef)
            },
            // Whether a property's type is one of the *ancestors* of its own container. Mirrors
            // `isAncestorField` / `isAncestorReturnType` but for property types.
            "isAncestorProperty" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeProperty && isTypeAncestor(limeElement.typeRef)
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
            // Whether a function/constructor throws (has a non-null exception type). Python exception
            // translation for `Return<T, Error>` is not wired yet (see Phase E/G7 of the Python
            // follow-up plan), so throwing functions are skipped in the pybind11 binding to avoid
            // emitting ambiguous overloads (e.g. a `create` static method colliding with the
            // all-fields `create`). The C++ and Dart generators still emit them.
            "isThrowing" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeFunction &&
                    limeElement.exception != null
            },
            // Whether the C++ return type of a function contains a comma (e.g. a `std::map<K, V>` or
            // `std::pair<A, B>` instantiation). The `PYBIND11_OVERRIDE_PURE` / `PYBIND11_OVERRIDE`
            // macros are not variadic in their type argument, so a comma-bearing return type must be
            // aliased through a `using` declaration before being passed to the macro. Accepts either
            // the function itself or its return type reference as the predicate context.
            "returnTypeHasComma" to { limeElement: Any ->
                val typeRef =
                    when (limeElement) {
                        is com.here.gluecodium.model.lime.LimeFunction -> limeElement.returnType.typeRef
                        is com.here.gluecodium.model.lime.LimeTypeRef -> limeElement
                        is com.here.gluecodium.model.lime.LimeProperty -> limeElement.typeRef
                        else -> null
                    }
                typeRef != null && pybind11NameResolver.resolveName(typeRef).contains(',')
            },
            // Whether a struct needs a `py::init<>()` with no arguments. Mirrors the C++ generator's
            // `hasDefaultConstructor` predicate: the C++ struct is default-constructible unless it is
            // immutable, has an explicit no-arg field constructor, or has an uninitialized field
            // whose (recursively expanded) type is immutable. An explicit no-arg field constructor
            // already yields the same `py::init<>()`, so it is suppressed here to avoid registering a
            // duplicate constructor in pybind11.
            "hasDefaultConstructor" to { limeElement: Any ->
                when {
                    limeElement !is com.here.gluecodium.model.lime.LimeStruct -> false
                    limeElement.fieldConstructors.any { it.fieldRefs.isEmpty() } -> false
                    limeElement.uninitializedFields.isEmpty() -> true
                    limeElement.uninitializedFields
                        .flatMap { com.here.gluecodium.generator.common.CommonGeneratorPredicates.getAllFieldTypes(it.typeRef.type) }
                        .any { it.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) } -> false
                    !limeElement.attributes.have(com.here.gluecodium.model.lime.LimeAttributeType.IMMUTABLE) -> true
                    else -> false
                }
            },
            // Whether a struct needs a `py::init<...>()` taking every field. True when the struct
            // has no explicit field constructors (so the implicit all-fields constructor is the
            // only one) or, for immutable structs, when no all-fields field constructor is declared.
            "needsAllFieldsConstructor" to { limeElement: Any ->
                when {
                    limeElement !is com.here.gluecodium.model.lime.LimeStruct -> false
                    // A default constructor (all fields defaulted) already covers the no-arg case,
                    // so the all-fields constructor would be a redundant duplicate py::init<>().
                    limeElement.uninitializedFields.isEmpty() -> false
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
        return limeField.path.parent.allParents.any { limeReferenceMap[it.toString()]?.let { e -> (e as? LimeNamedElement)?.fullName } == fieldTypeName }
    }

    private fun isTypeAncestor(limeTypeRef: LimeTypeRef): Boolean {
        val typeName = (limeTypeRef.type.actualType as? LimeNamedElement)?.fullName ?: return false
        // Walk up from the type reference's container to find any ancestor matching the referenced
        // type. Use `tailParents` (which terminates once the tail is exhausted) instead of a manual
        // `parent` walk: `LimePath.parent` is idempotent for an empty tail, so a hand-rolled
        // `while (currentKey != null)` loop would never terminate when no ancestor matches, causing
        // the generator to spin indefinitely on deeply nested types.
        return limeTypeRef.type.path.parent.tailParents.any {
            (limeReferenceMap[it.toString()] as? LimeNamedElement)?.fullName == typeName
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
}
