/*
 * Copyright (C) 2016-2019 HERE Europe B.V.
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

package com.here.genium.generator.cbridge

import com.here.genium.common.ModelBuilderContextStack
import com.here.genium.generator.common.modelbuilder.AbstractLimeBasedModelBuilder
import com.here.genium.generator.cpp.CppIncludeResolver
import com.here.genium.generator.cpp.CppLibraryIncludes
import com.here.genium.generator.cpp.CppModelBuilder
import com.here.genium.generator.cpp.CppTypeMapper
import com.here.genium.generator.swift.SwiftModelBuilder
import com.here.genium.model.cbridge.CArray
import com.here.genium.model.cbridge.CBridgeIncludeResolver
import com.here.genium.model.cbridge.CElement
import com.here.genium.model.cbridge.CEnum
import com.here.genium.model.cbridge.CField
import com.here.genium.model.cbridge.CFunction
import com.here.genium.model.cbridge.CInterface
import com.here.genium.model.cbridge.CMap
import com.here.genium.model.cbridge.CParameter
import com.here.genium.model.cbridge.CSet
import com.here.genium.model.cbridge.CStruct
import com.here.genium.model.cbridge.CType
import com.here.genium.model.common.Include
import com.here.genium.model.cpp.CppField
import com.here.genium.model.cpp.CppMethod
import com.here.genium.model.cpp.CppParameter
import com.here.genium.model.cpp.CppStruct
import com.here.genium.model.lime.LimeAttributeType
import com.here.genium.model.lime.LimeAttributeType.CPP
import com.here.genium.model.lime.LimeAttributeValueType
import com.here.genium.model.lime.LimeAttributeValueType.EXTERNAL_GETTER
import com.here.genium.model.lime.LimeAttributeValueType.EXTERNAL_SETTER
import com.here.genium.model.lime.LimeContainer
import com.here.genium.model.lime.LimeElement
import com.here.genium.model.lime.LimeEnumeration
import com.here.genium.model.lime.LimeField
import com.here.genium.model.lime.LimeMap
import com.here.genium.model.lime.LimeMethod
import com.here.genium.model.lime.LimeNamedElement
import com.here.genium.model.lime.LimeParameter
import com.here.genium.model.lime.LimeProperty
import com.here.genium.model.lime.LimeSet
import com.here.genium.model.lime.LimeStruct
import com.here.genium.model.lime.LimeType
import com.here.genium.model.lime.LimeTypeDef
import com.here.genium.model.lime.LimeTypeHelper
import com.here.genium.model.lime.LimeTypeRef
import com.here.genium.model.swift.SwiftField
import com.here.genium.model.swift.SwiftMethod
import com.here.genium.model.swift.SwiftParameter
import com.here.genium.model.swift.SwiftProperty

class CBridgeModelBuilder(
    contextStack: ModelBuilderContextStack<CElement> = ModelBuilderContextStack(),
    private val limeReferenceMap: Map<String, LimeElement>,
    private val includeResolver: CBridgeIncludeResolver,
    private val cppIncludeResolver: CppIncludeResolver,
    private val cppBuilder: CppModelBuilder,
    private val swiftBuilder: SwiftModelBuilder,
    private val typeMapper: CBridgeTypeMapper,
    private val internalNamespace: List<String>
) : AbstractLimeBasedModelBuilder<CElement>(contextStack) {

    val arraysCollector = mutableMapOf<String, CArray>()

    override fun startBuilding(limeContainer: LimeContainer) {
        openContext()
        if (limeContainer.type != LimeContainer.ContainerType.TYPE_COLLECTION) {
            val cppTypeInfo =
                typeMapper.createCustomTypeInfo(limeContainer, CppTypeInfo.TypeCategory.CLASS)
            storeResult(cppTypeInfo)
        }
    }

    override fun startBuilding(limeStruct: LimeStruct) {
        openContext()
        val cppTypeInfo =
            typeMapper.createCustomTypeInfo(limeStruct, CppTypeInfo.TypeCategory.STRUCT)
        storeResult(cppTypeInfo)
    }

    override fun finishBuilding(limeContainer: LimeContainer) {
        val parentClass = getPreviousResultOrNull(CInterface::class.java)
        val inheritedFunctions = mutableListOf<CFunction>()
        if (parentClass != null) {
            inheritedFunctions.addAll(parentClass.inheritedFunctions)
            inheritedFunctions.addAll(parentClass.functions)
        }

        val cInterface = CInterface(
            name = CBridgeNameRules.getInterfaceName(limeContainer),
            selfType = currentContext.currentResults.filterIsInstance<CppTypeInfo>().firstOrNull(),
            internalNamespace = internalNamespace,
            structs = getPreviousResults(CStruct::class.java),
            enums = getPreviousResults(CEnum::class.java),
            maps = getPreviousResults(CMap::class.java),
            sets = getPreviousResults(CSet::class.java),
            functions = getPreviousResults(CFunction::class.java),
            inheritedFunctions = inheritedFunctions,
            functionTableName = if (limeContainer.type == LimeContainer.ContainerType.INTERFACE)
                CBridgeNameRules.getFunctionTableName(limeContainer) else null,
            isEquatable = limeContainer.attributes.have(LimeAttributeType.EQUATABLE),
            isPointerEquatable = limeContainer.attributes.have(LimeAttributeType.POINTER_EQUATABLE)
        )

        cInterface.headerIncludes.addAll(CBridgeComponents.collectHeaderIncludes(cInterface))
        cInterface.implementationIncludes.addAll(
            CBridgeComponents.collectImplementationIncludes(cInterface)
        )
        cInterface.implementationIncludes.add(includeResolver.resolveInclude(limeContainer))
        CppLibraryIncludes.filterIncludes(cInterface.implementationIncludes, internalNamespace)
        cInterface.privateHeaderIncludes.addAll(
            CBridgeComponents.collectPrivateHeaderIncludes(cInterface)
        )

        if (limeContainer.type == LimeContainer.ContainerType.INTERFACE) {
            cInterface.implementationIncludes.add(
                Include.createInternalInclude(CBridgeComponents.PROXY_CACHE_FILENAME)
            )
        }

        storeResult(cInterface)
        closeContext()
    }

    override fun finishBuilding(limeMethod: LimeMethod) {
        var parameterSelf: CParameter? = null
        if (!limeMethod.isStatic) {
            val cppTypeInfo = parentContext!!.currentResults.filterIsInstance<CppTypeInfo>().first()
            parameterSelf = CParameter("_instance", cppTypeInfo)
        }

        val swiftMethod = swiftBuilder.getFinalResult(SwiftMethod::class.java)
        val cppMethod = cppBuilder.getFinalResult(CppMethod::class.java)
        val limeParent =
            limeReferenceMap[limeMethod.path.parent.toString()] as LimeNamedElement
        val returnType = when {
            limeParent !is LimeStruct && limeMethod.isConstructor ->
                typeMapper.createCustomTypeInfo(limeParent, CppTypeInfo.TypeCategory.CLASS)
            else -> {
                val cppTypeInfo = mapType(limeMethod.returnType.typeRef.type)
                if (limeMethod.returnType.typeRef.isNullable) {
                    CBridgeTypeMapper.createNullableTypeInfo(cppTypeInfo, cppMethod.returnType)
                } else {
                    cppTypeInfo
                }
            }
        }

        var errorType: CppTypeInfo? = null
        val limeErrorType = limeMethod.exception?.errorEnum
        if (limeErrorType != null) {
            errorType = typeMapper.createEnumTypeInfo(limeErrorType.type, asErrorType = true)
        }

        val result = CFunction(
            swiftMethod.cShortName,
            swiftMethod.cNestedSpecifier,
            returnType,
            getPreviousResults(CParameter::class.java),
            parameterSelf,
            cppMethod.fullyQualifiedName,
            cppIncludeResolver.resolveIncludes(limeMethod).toSet(),
            cppMethod.name,
            cppMethod.returnType.fullyQualifiedName,
            limeMethod.attributes.have(CPP, LimeAttributeValueType.CONST),
            errorType
        )

        storeResult(result)
        closeContext()
    }

    override fun finishBuilding(limeParameter: LimeParameter) {
        var cppTypeInfo = getPreviousResult(CppTypeInfo::class.java)
        if (limeParameter.typeRef.isNullable) {
            val cppParameter = cppBuilder.getFinalResult(CppParameter::class.java)
            cppTypeInfo = CBridgeTypeMapper.createNullableTypeInfo(cppTypeInfo, cppParameter.type)
        }
        val swiftParameter = swiftBuilder.getFinalResult(SwiftParameter::class.java)
        val result = CParameter(swiftParameter.name, cppTypeInfo)

        storeResult(result)
        closeContext()
    }

    override fun finishBuilding(limeStruct: LimeStruct) {
        val cppStruct = cppBuilder.getFinalResult(CppStruct::class.java)
        val cStruct = CStruct(
            CBridgeNameRules.getTypeName(limeStruct),
            cppStruct.fullyQualifiedName,
            currentContext.currentResults.filterIsInstance<CppTypeInfo>().first(),
            cppStruct.hasImmutableFields,
            getPreviousResults(CField::class.java),
            getPreviousResults(CFunction::class.java)
        )

        storeResult(cStruct)
        closeContext()
    }

    override fun finishBuilding(limeField: LimeField) {
        val cppField = cppBuilder.getFinalResult(CppField::class.java)
        val swiftField = swiftBuilder.getFinalResult(SwiftField::class.java)

        var cppTypeInfo = getPreviousResult(CppTypeInfo::class.java)
        if (limeField.typeRef.isNullable) {
            cppTypeInfo = CBridgeTypeMapper.createNullableTypeInfo(cppTypeInfo, cppField.type)
        }

        val cField = CField(
            swiftField.name,
            cppField.name,
            cppTypeInfo,
            limeField.attributes.get(CPP, EXTERNAL_GETTER, String::class.java),
            limeField.attributes.get(CPP, EXTERNAL_SETTER, String::class.java)
        )

        storeResult(cField)
        closeContext()
    }

    override fun finishBuilding(limeEnumeration: LimeEnumeration) {
        val result = CEnum(
            CBridgeNameRules.getTypeName(limeEnumeration),
            typeMapper.createEnumTypeInfo(limeEnumeration)
        )

        storeResult(result)
        closeContext()
    }

    override fun finishBuilding(limeProperty: LimeProperty) {
        val cppMethods = cppBuilder.finalResults.filterIsInstance<CppMethod>()
        val swiftProperty = swiftBuilder.getFinalResult(SwiftProperty::class.java)

        val classInfo = parentContext!!.currentResults.filterIsInstance<CppTypeInfo>().first()
        val selfParameter = when {
            limeProperty.isStatic -> null
            else -> CParameter("_instance", classInfo)
        }

        val cppGetterMethod = cppMethods.first()
        var attributeTypeInfo = getPreviousResult(CppTypeInfo::class.java)
        if (limeProperty.typeRef.isNullable) {
            attributeTypeInfo = CBridgeTypeMapper.createNullableTypeInfo(
                attributeTypeInfo,
                cppGetterMethod.returnType
            )
        }

        val getterSwiftMethod = swiftProperty.getter
        val getterFunction = CFunction(
            getterSwiftMethod.cShortName,
            getterSwiftMethod.cNestedSpecifier,
            attributeTypeInfo,
            emptyList(),
            selfParameter,
            cppGetterMethod.fullyQualifiedName,
            cppIncludeResolver.resolveIncludes(limeProperty).toSet(),
            cppGetterMethod.name,
            cppGetterMethod.returnType.fullyQualifiedName,
            true
        )
        storeResult(getterFunction)

        if (limeProperty.setter != null) {
            val setterSwiftMethod = swiftProperty.setter
            val cppSetterMethod = cppMethods[1]
            val setterFunction = CFunction(
                setterSwiftMethod.cShortName,
                setterSwiftMethod.cNestedSpecifier,
                CppTypeInfo(CType.VOID),
                listOf(CParameter("newValue", attributeTypeInfo)),
                selfParameter,
                cppSetterMethod.fullyQualifiedName,
                cppIncludeResolver.resolveIncludes(limeProperty).toSet(),
                cppSetterMethod.name,
                cppSetterMethod.returnType.fullyQualifiedName
            )
            storeResult(setterFunction)
        }

        closeContext()
    }

    override fun finishBuilding(limeTypeDef: LimeTypeDef) {
        val limeActualType = LimeTypeHelper.getActualType(limeTypeDef.typeRef.type)
        if (limeActualType is LimeMap) {
            val keyType = mapType(limeActualType.keyType.type)
            val valueType = mapType(limeActualType.valueType.type)

            val cMap = CMap(
                CBridgeNameRules.getTypeName(limeTypeDef),
                keyType,
                valueType,
                cppIncludeResolver.resolveIncludes(limeTypeDef).first(),
                CppTypeMapper.hasStdHash(limeActualType.keyType)
            )

            storeResult(cMap)
        } else if (limeActualType is LimeSet) {
            val elementType = mapType(limeActualType.elementType.type)
            val cSet = CSet(
                CBridgeNameRules.getTypeName(limeTypeDef),
                elementType,
                cppIncludeResolver.resolveIncludes(limeTypeDef).first(),
                CppTypeMapper.hasStdHash(limeActualType.elementType)
            )
            storeResult(cSet)
        }

        closeContext()
    }

    override fun finishBuilding(limeTypeRef: LimeTypeRef) {
        val cppTypeInfo = mapType(limeTypeRef.type)

        storeResult(cppTypeInfo)
        closeContext()
    }

    private fun mapType(limeType: LimeType): CppTypeInfo {
        val cppTypeInfo = typeMapper.mapType(limeType)
        if (cppTypeInfo is CppArrayTypeInfo) {
            val arrayName = CBridgeNameResolver.getArrayName(limeType)
            arraysCollector.putIfAbsent(arrayName, CArray(arrayName, cppTypeInfo))
        }

        return cppTypeInfo
    }
}
