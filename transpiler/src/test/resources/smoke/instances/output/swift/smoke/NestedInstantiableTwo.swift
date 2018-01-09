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


internal func getRef(_ ref: NestedInstantiableTwo) -> RefHolder<smoke_NestedInstantiableTwoRef> {
    return RefHolder<smoke_NestedInstantiableTwoRef>(ref.c_instance)
}
public class NestedInstantiableTwo {
    let c_instance : smoke_NestedInstantiableTwoRef

    public init?(cNestedInstantiableTwo: smoke_NestedInstantiableTwoRef) {
        c_instance = cNestedInstantiableTwo
    }

    deinit {
        smoke_NestedInstantiableTwo_release(c_instance)
    }
    public func setMultipleTypeInstances(instanceOne: SimpleInstantiableOne, instanceTwo: SimpleInstantiableTwo, nestedInstantiable: NestedInstantiableOne) -> Void {
        let instanceOneHandle = getRef(instanceOne)
        let instanceTwoHandle = getRef(instanceTwo)
        let nestedInstantiableHandle = getRef(nestedInstantiable)
        return smoke_NestedInstantiableTwo_setMultipleTypeInstances(c_instance, instanceOneHandle.ref, instanceTwoHandle.ref, nestedInstantiableHandle.ref)
    }

    public func getInstantiableOne() -> SimpleInstantiableOne? {
        let cResult = smoke_NestedInstantiableTwo_getInstantiableOne(c_instance)
        precondition(cResult.private_pointer != nil, "Out of memory")

        return SimpleInstantiableOne(cSimpleInstantiableOne: cResult)
    }

    public func getInstantiableTwo() -> SimpleInstantiableTwo? {
        let cResult = smoke_NestedInstantiableTwo_getInstantiableTwo(c_instance)
        precondition(cResult.private_pointer != nil, "Out of memory")

        return SimpleInstantiableTwo(cSimpleInstantiableTwo: cResult)
    }

    public func getNestedInstantiable() -> NestedInstantiableOne? {
        let cResult = smoke_NestedInstantiableTwo_getNestedInstantiable(c_instance)
        precondition(cResult.private_pointer != nil, "Out of memory")

        return NestedInstantiableOne(cNestedInstantiableOne: cResult)
    }

    public func setSelfInstantiable(selfInstance: NestedInstantiableTwo) -> Void {
        let selfInstanceHandle = getRef(selfInstance)
        return smoke_NestedInstantiableTwo_setSelfInstantiable(c_instance, selfInstanceHandle.ref)
    }

    public func getSelfInstantiable() -> NestedInstantiableTwo? {
        let cResult = smoke_NestedInstantiableTwo_getSelfInstantiable(c_instance)
        precondition(cResult.private_pointer != nil, "Out of memory")

        return NestedInstantiableTwo(cNestedInstantiableTwo: cResult)
    }

}
