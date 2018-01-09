//
// Copyright (C) 2017 HERE Global B.V. and/or its affiliated companies. All rights reserved.
//
// This software, including documentation, is protected by copyright controlled by
// HERE Global B.V. All rights are reserved. Copying, including reproducing, storing,
// adapting or translating, any or all of this material requires the prior written
// consent of HERE Global B.V. This material also contains confidential information,
// which may not be disclosed to others without prior written consent of HERE Global B.V.
//
// Automatically generated. Do not modify. Your changes will be lost.

import Foundation


internal func getRef(_ ref: NestedInstantiableOne) -> RefHolder<smoke_NestedInstantiableOneRef> {
    return RefHolder<smoke_NestedInstantiableOneRef>(ref.c_instance)
}
public class NestedInstantiableOne {
    let c_instance : smoke_NestedInstantiableOneRef

    public init?(cNestedInstantiableOne: smoke_NestedInstantiableOneRef) {
        c_instance = cNestedInstantiableOne
    }

    deinit {
        smoke_NestedInstantiableOne_release(c_instance)
    }
    public func setSameTypeInstances(instanceOne: SimpleInstantiableOne, instanceTwo: SimpleInstantiableOne) -> Void {
        let instanceOneHandle = getRef(instanceOne)
        let instanceTwoHandle = getRef(instanceTwo)
        return smoke_NestedInstantiableOne_setSameTypeInstances(c_instance, instanceOneHandle.ref, instanceTwoHandle.ref)
    }

    public func getInstanceOne() -> SimpleInstantiableOne? {
        let cResult = smoke_NestedInstantiableOne_getInstanceOne(c_instance)
        precondition(cResult.private_pointer != nil, "Out of memory")

        return SimpleInstantiableOne(cSimpleInstantiableOne: cResult)
    }

    public func getInstanceTwo() -> SimpleInstantiableOne? {
        let cResult = smoke_NestedInstantiableOne_getInstanceTwo(c_instance)
        precondition(cResult.private_pointer != nil, "Out of memory")

        return SimpleInstantiableOne(cSimpleInstantiableOne: cResult)
    }

}
