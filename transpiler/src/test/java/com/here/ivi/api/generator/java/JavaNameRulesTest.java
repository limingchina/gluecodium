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

import static org.junit.Assert.assertEquals;

import com.here.ivi.api.model.java.JavaClass;
import com.here.ivi.api.model.java.JavaExceptionClass;
import com.here.ivi.api.model.java.JavaPackage;
import com.here.ivi.api.platform.android.AndroidGeneratorSuite;
import java.util.Arrays;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

@RunWith(JUnit4.class)
public final class JavaNameRulesTest {
  @Rule public final ExpectedException expectedException = ExpectedException.none();

  @Test
  public void getFileName() {
    // Arrange
    JavaClass javaClass = new JavaClass("MyClass");

    // Act
    String javaFile = JavaNameRules.getFileName(javaClass);

    // Assert
    assertEquals(AndroidGeneratorSuite.GENERATOR_NAME + "/com/example/MyClass.java", javaFile);
  }

  @Test
  public void getFileNameThrowsForNullClass() {
    // Arrange, act, assert
    expectedException.expect(NullPointerException.class);
    JavaNameRules.getFileName(null);
  }

  @Test
  public void getFileNameForExceptionClass() {
    // Arrange
    JavaPackage javaPackage = new JavaPackage(Arrays.asList("com", "example", "generator"));
    JavaExceptionClass javaExceptionClass =
        new JavaExceptionClass("ExceptionalException", null, javaPackage);

    // Act
    String javaFile = JavaNameRules.getFileName(javaExceptionClass);

    // Assert
    assertEquals(
        AndroidGeneratorSuite.GENERATOR_NAME + "/com/example/generator/ExceptionalException.java",
        javaFile);
  }
}
