/*
 * Copyright (C) 2017 HERE Global B.V. and its affiliate(s). All rights reserved.
 *
 * This software, including documentation, is protected by copyright controlled by
 * HERE Global B.V. All rights are reserved. Copying, including reproducing, storing,
 * adapting or translating, any or all of this material requires the prior written
 * consent of HERE Global B.V. This material also contains confidential information,
 * which may not be disclosed to others without prior written consent of HERE Global B.V.
 *
 */

package com.here.ivi.api.generator.cpp;

import com.google.common.annotations.VisibleForTesting;
import com.here.ivi.api.TranspilerExecutionException;
import com.here.ivi.api.model.cppmodel.*;
import com.here.ivi.api.model.rules.InstanceRules;
import org.franca.core.franca.FArrayType;
import org.franca.core.franca.FBasicTypeId;
import org.franca.core.franca.FEnumerationType;
import org.franca.core.franca.FMapType;
import org.franca.core.franca.FStructType;
import org.franca.core.franca.FType;
import org.franca.core.franca.FTypeDef;
import org.franca.core.franca.FTypeRef;
import org.franca.core.franca.FUnionType;

public class CppTypeMapper {

  private static final CppTypeRef BASIC_STRING_CHAR_TYPE =
      CppTemplateTypeRef.create(
          CppTemplateTypeRef.TemplateClass.BASIC_STRING, CppPrimitiveTypeRef.CHAR);

  @VisibleForTesting
  static final CppTypeRef STRING_TYPE =
      new CppTypeDefRef("::std::string", BASIC_STRING_CHAR_TYPE, BASIC_STRING_CHAR_TYPE.includes);

  private final CppIncludeResolver includeResolver;

  public CppTypeMapper(final CppIncludeResolver includeResolver) {
    this.includeResolver = includeResolver;
  }

  public CppTypeRef map(FTypeRef type) {
    if (type.getDerived() != null) {
      return mapDerived(type.getDerived());
    }
    if (type.getPredefined() != FBasicTypeId.UNDEFINED) {
      return mapPredefined(type);
    }

    if (type.getInterval() != null) {
      throw new TranspilerExecutionException(
          "The transpiler does not support integer ranges. "
              + "Please use regular Integer types like Int64 instead. Type: "
              + type);
    }

    throw new TranspilerExecutionException("Unmapped ftype ref" + type);
  }

  private CppTypeRef mapDerived(FType derived) {
    if (derived instanceof FTypeDef) {
      return mapTypeDef((FTypeDef) derived);
    }
    if (derived instanceof FArrayType) {
      return mapArray((FArrayType) derived);
    }
    if (derived instanceof FMapType) {
      return mapMapType((FMapType) derived);
    }
    if (derived instanceof FStructType) {
      return mapStruct((FStructType) derived);
    }
    if (derived instanceof FEnumerationType) {
      return mapEnum((FEnumerationType) derived);
    }
    if (derived instanceof FUnionType) {
      return mapUnion((FUnionType) derived);
    }
    throw new TranspilerExecutionException("Unmapped derived type: " + derived.getName());
  }

  private CppTypeRef mapTypeDef(FTypeDef typedef) {
    String fullyQualifiedName = CppNameRules.getFullyQualifiedName(typedef);

    if (InstanceRules.isInstanceId(typedef)) {
      CppComplexTypeRef instanceType =
          new CppComplexTypeRef.Builder(fullyQualifiedName)
              .includes(includeResolver.resolveInclude(typedef))
              .build();

      return CppTemplateTypeRef.create(
          CppTemplateTypeRef.TemplateClass.SHARED_POINTER, instanceType);
    } else {

      CppTypeRef actualType = map(typedef.getActualType());

      return new CppTypeDefRef(
          fullyQualifiedName, actualType, includeResolver.resolveInclude(typedef));
    }
  }

  public CppComplexTypeRef mapArray(final FArrayType array) {
    CppTypeRef elementType = map(array.getElementType());
    return CppTemplateTypeRef.create(CppTemplateTypeRef.TemplateClass.VECTOR, elementType);
  }

  public CppComplexTypeRef mapMapType(FMapType francaMapType) {

    CppTypeRef key = map(francaMapType.getKeyType());
    CppTypeRef value = map(francaMapType.getValueType());

    return CppTemplateTypeRef.create(CppTemplateTypeRef.TemplateClass.MAP, key, value);
  }

  public CppComplexTypeRef mapStruct(FStructType struct) {

    String fullyQualifiedName = CppNameRules.getFullyQualifiedName(struct);

    return new CppComplexTypeRef.Builder(fullyQualifiedName)
        .includes(includeResolver.resolveInclude(struct))
        .build();
  }

  public CppComplexTypeRef mapEnum(FEnumerationType enumeration) {

    String fullyQualifiedName = CppNameRules.getFullyQualifiedName(enumeration);

    return new CppComplexTypeRef.Builder(fullyQualifiedName)
        .typeInfo(CppTypeInfo.Enumeration)
        .includes(includeResolver.resolveInclude(enumeration))
        .build();
  }

  private CppComplexTypeRef mapUnion(FUnionType union) {
    String fullyQualifiedName = CppNameRules.getFullyQualifiedName(union);

    return new CppComplexTypeRef.Builder(fullyQualifiedName)
        .includes(includeResolver.resolveInclude(union))
        .build();
  }

  private static CppTypeRef mapPredefined(final FTypeRef type) {

    switch (type.getPredefined().getValue()) {
      case FBasicTypeId.BOOLEAN_VALUE:
        return CppPrimitiveTypeRef.BOOL;

      case FBasicTypeId.FLOAT_VALUE:
        return CppPrimitiveTypeRef.FLOAT;

      case FBasicTypeId.DOUBLE_VALUE:
        return CppPrimitiveTypeRef.DOUBLE;

      case FBasicTypeId.INT8_VALUE:
        return CppPrimitiveTypeRef.INT8;

      case FBasicTypeId.INT16_VALUE:
        return CppPrimitiveTypeRef.INT16;

      case FBasicTypeId.INT32_VALUE:
        return CppPrimitiveTypeRef.INT32;

      case FBasicTypeId.INT64_VALUE:
        return CppPrimitiveTypeRef.INT64;

      case FBasicTypeId.UINT8_VALUE:
        return CppPrimitiveTypeRef.UINT8;

      case FBasicTypeId.UINT16_VALUE:
        return CppPrimitiveTypeRef.UINT16;

      case FBasicTypeId.UINT32_VALUE:
        return CppPrimitiveTypeRef.UINT32;

      case FBasicTypeId.UINT64_VALUE:
        return CppPrimitiveTypeRef.UINT64;

      case FBasicTypeId.STRING_VALUE:
        return STRING_TYPE;

      case FBasicTypeId.BYTE_BUFFER_VALUE:
        return CppTemplateTypeRef.create(
            CppTemplateTypeRef.TemplateClass.VECTOR, CppPrimitiveTypeRef.UINT8);

      default:
        throw new TranspilerExecutionException(
            "unmapped predefined [" + type.getPredefined().getName() + "]");
    }
  }
}
