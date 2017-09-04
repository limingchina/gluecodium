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

import com.here.ivi.api.generator.baseapi.BaseApiGeneratorSuite;
import com.here.ivi.api.generator.common.NameHelper;
import com.here.ivi.api.model.franca.DefinedBy;
import com.here.ivi.api.model.franca.FrancaElement;
import com.here.ivi.api.model.franca.Interface;
import java.io.File;
import java.util.List;
import org.eclipse.emf.ecore.EObject;
import org.franca.core.franca.FCompoundType;
import org.franca.core.franca.FInterface;

public final class CppNameRules {

  private CppNameRules() {}

  public static String getCppTypename(String baseName) {
    return baseName;
  }

  public static String getTypeCollectionName(String typeCollectionName) {
    return typeCollectionName.toLowerCase(); // mytypecollection
  }

  public static String getMethodName(String base) {
    return NameHelper.toLowerCamelCase(base); // doStuff
  }

  public static String getEnumName(String base) {
    return NameHelper.toUpperCamelCase(base); // MyEnum
  }

  public static String getStructName(String base) {
    return NameHelper.toUpperCamelCase(base); // MyStruct
  }

  public static String getTypedefName(String base) {
    return NameHelper.toUpperCamelCase(base); // MyTypedef
  }

  public static String getHeaderFileSuffix() {
    return ".h";
  }

  public static List<String> getNestedNameSpecifier(EObject type) {
    DefinedBy definer = DefinedBy.createFromFModelElement(type);
    List<String> result = getNamespace(definer);
    // special rule for structs defined in interfaces ...
    if (definer.type instanceof FInterface) {
      result.add(getClassName(definer.type.getName()));
    } else {
      // common rule for all other types
      result.add(getTypeCollectionName(definer.type.getName()));
    }
    return result;
  }

  public static String getFullyQualifiedName(FCompoundType francaCompoundType) {
    List<String> nestedNameSpecifier = getNestedNameSpecifier(francaCompoundType);
    String compoundName = getStructName(francaCompoundType.getName());

    return nestedNameSpecifier.isEmpty()
        ? "::" + compoundName
        : "::" + String.join("::", nestedNameSpecifier) + "::" + compoundName;
  }

  public static List<String> getNamespace(DefinedBy definer) {
    return definer.getPackages();
  }

  public static String getClassName(String typeCollectionName) {
    return NameHelper.toUpperCamelCase(typeCollectionName);
  }

  public static String getEnumEntryName(String base) {
    return NameHelper.toUpperCamelCase(base); // MyEnumEntry
  }

  public static String getFieldName(String base) {
    return NameHelper.toLowerCamelCase(base); // myField
  }

  public static String getConstantName(String base) {
    return NameHelper.toUpperCamelCase(base); // MyConstant
  }

  public static String getHeaderPath(FrancaElement francaElement) {
    return BaseApiGeneratorSuite.GENERATOR_NAME
        + File.separator
        + String.join(File.separator, francaElement.getPackageNames())
        + File.separator
        + (francaElement instanceof Interface
            ? getClassName(((Interface) francaElement).getFrancaInterface().getName())
            : francaElement.getFrancaTypeCollection().getName())
        + getHeaderFileSuffix();
  }
}
