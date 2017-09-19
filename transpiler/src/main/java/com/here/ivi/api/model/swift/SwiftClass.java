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

package com.here.ivi.api.model.swift;

import static java.util.Collections.emptyList;

import java.util.ArrayList;
import java.util.List;

public final class SwiftClass extends SwiftModelElement {

  public String comment;
  public final String parentClass;
  public List<String> implementsProtocols;
  public List<SwiftProperty> properties;
  public List<SwiftMethod> methods;
  public List<SwiftContainerType> structs;
  public List<SwiftEnum> enums;
  public String nameSpace;
  public String cInstanceRef;
  public String cInstance;

  public SwiftClass(String className, String parentClassName) {
    super(className);
    this.parentClass = parentClassName;
    this.implementsProtocols = emptyList();
    this.properties = emptyList();
    this.methods = emptyList();
    this.structs = emptyList();
    this.enums = new ArrayList<>();
    this.comment = "";
    this.nameSpace = "";
  }

  public SwiftClass(String className) {
    this(className, null);
  }

  public boolean needClassDefinition() {
    return (implementsProtocols != null && !implementsProtocols.isEmpty())
        || (parentClass != null && !parentClass.isEmpty());
  }

  public boolean isStatic() {
    return methods
        .stream()
        .anyMatch(
            s -> {
              return s.isStatic;
            });
  }
}
