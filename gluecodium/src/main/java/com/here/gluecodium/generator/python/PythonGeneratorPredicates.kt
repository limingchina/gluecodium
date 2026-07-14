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
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSignatureResolver
import com.here.gluecodium.model.lime.LimeStruct
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
            "needsInterfaceLambdaBinding" to { limeFunction: Any ->
                limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
                    !limeFunction.isStatic &&
                    limeReferenceMap[limeFunction.path.parent.toString()] is
                        com.here.gluecodium.model.lime.LimeInterface
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
            // Whether a struct needs a `py::init<>()` with no arguments. True when every field has
            // a default value (or there are no fields), so the C++ struct is default-constructible.
            "hasDefaultConstructor" to { limeElement: Any ->
                limeElement is com.here.gluecodium.model.lime.LimeStruct &&
                    limeElement.uninitializedFields.isEmpty()
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
        )
}
