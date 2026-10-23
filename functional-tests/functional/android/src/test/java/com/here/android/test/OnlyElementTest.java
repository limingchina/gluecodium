/*
 * Copyright (C) 2016-2026 HERE Europe B.V.
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
package com.here.android.test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;

import android.os.Build;
import com.here.android.RobolectricApplication;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = Build.VERSION_CODES.M, application = RobolectricApplication.class)
public final class OnlyElementTest {
  @Test
  public void selectedMethodsRoundTrip() {
    String input = "Only: Java round trip";
    assertEquals(input, OnlyFunctions.shared(input));
  }

  @Test
  public void otherPlatformsAreExcluded() throws Exception {
    // The Kotlin functional build can reuse the Java test sources.
    boolean isKotlin = false;
    for (Class<?> nestedClass : OnlyFunctions.class.getDeclaredClasses()) {
      isKotlin |= nestedClass.getSimpleName().equals("Companion");
    }
    String selectedPlatform = isKotlin ? "kotlin" : "java";
    String excludedPlatform = isKotlin ? "java" : "kotlin";
    assertNotNull(OnlyFunctions.class.getDeclaredMethod(selectedPlatform + "Only", String.class));
    String selectedConstant = selectedPlatform.toUpperCase(Locale.ROOT) + "_CONSTANT";
    assertEquals(isKotlin ? 22 : 11,
        OnlyFunctions.class.getDeclaredField(selectedConstant).getInt(null));
    Set<String> excludedMethods = new HashSet<>(Arrays.asList(
        excludedPlatform + "Only", "swiftOnly", "dartOnly", "cppOnly"));
    Set<String> excludedConstants = new HashSet<>(Arrays.asList(
        excludedPlatform.toUpperCase(Locale.ROOT) + "_CONSTANT",
        "SWIFT_CONSTANT", "DART_CONSTANT", "CPP_CONSTANT"));
    for (Method method : OnlyFunctions.class.getDeclaredMethods()) {
      assertFalse(excludedMethods.contains(method.getName()));
    }
    for (Field field : OnlyFunctions.class.getDeclaredFields()) {
      assertFalse(excludedConstants.contains(field.getName()));
    }
  }
}
