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

package com.here.ivi.api.test;

import static org.junit.Assert.assertTrue;

import java.util.Collection;

public class Assert {

  public static <E> void assertContains(Collection<E> container, E element) {
    assertTrue(container + " must contain " + element, container.contains(element));
  }

  public static <E> void assertContainsAll(Collection<E> container, Collection<E> elements) {
    assertTrue(container + " must contain all " + elements, container.containsAll(elements));
  }
}
