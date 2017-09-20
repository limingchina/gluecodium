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

package com.here.ivi.api.generator.java;

import com.here.ivi.api.generator.android.AndroidGeneratorSuite;
import com.here.ivi.api.generator.common.NameHelper;
import com.here.ivi.api.model.javamodel.JavaTopLevelElement;
import java.io.File;
import java.util.List;

public final class JavaNameRules {
  public static final String JAVA_FILE_ENDING = ".java";

  private JavaNameRules() {}

  private static String formatPackageName(List<String> packageNames) {
    return packageNames.isEmpty() ? "" : String.join(File.separator, packageNames) + File.separator;
  }

  public static String getFileName(final JavaTopLevelElement javaElement) {
    return AndroidGeneratorSuite.GENERATOR_NAME
        + File.separator
        + formatPackageName(javaElement.javaPackage.packageNames)
        + javaElement.name
        + JAVA_FILE_ENDING;
  }

  public static String getClassName(String base) {
    return NameHelper.toUpperCamelCase(base);
  }

  public static String getImplementationClassName(String base) {
    return getClassName(base) + "Impl";
  }

  public static String getMethodName(final String base) {
    return NameHelper.toLowerCamelCase(base);
  }

  public static String getGetterName(final String base) {
    return "get" + NameHelper.toUpperCamelCase(base);
  }

  public static String getSetterName(final String base) {
    return "set" + NameHelper.toUpperCamelCase(base);
  }

  public static String getArgumentName(final String base) {
    return NameHelper.toLowerCamelCase(base);
  }

  public static String getConstantName(final String base) {
    return NameHelper.toUpperSnakeCase(base);
  }

  public static String getFieldName(final String base) {
    return NameHelper.toLowerCamelCase(base);
  }
}
